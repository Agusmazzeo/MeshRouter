import logging
from threading import Thread
import time
from queue import Queue

from digi.xbee.devices import DigiMeshDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
from dictdiffer import diff

from app.manager.device_manager import DeviceControl
from app.utils.models.device import DeviceModel
from app.utils.serial import SerialBitSize, SerialParity, SerialStopBits
from app.services.http import HTTPService
from config.classes import Config


class RouterService:

    def __init__(self, logger: logging.Logger):

        self.device_control_map = {}
        self.device_map = {}
        self.http_service = HTTPService(Config.get("server_url"), Config.get("router_id"))
        self.router = self.http_service.get_router_info()
        self.logger = logger
        
        # self.set_up_serial()
        self.set_up_xbee_gateway()
        self.set_up_message_queue()

        self.start_uart_sender()
        self.start_router_updater()
        

    @property
    def serial_uart(self):
        return self._serial_uart

    @property
    def xbee(self):
        return self._xbee

    @property
    def message_queue(self):
        return self._message_queue

    # def set_up_serial(self):
    #     serial_config = Config.get("serial_config")
    #     # self._serial_uart = serial.Serial(
    #     #     port=serial_config["port"],
    #     #     baudrate=serial_config["baud_rate"],
    #     #     parity=SerialParity[serial_config["parity"]].value,
    #     #     stopbits=SerialStopBits[serial_config["stopbits"]].value,
    #     #     bytesize=SerialBitSize[serial_config["bytesize"]].value,
    #     #     timeout=serial_config["timeout"]
    #     # )
    #     self._serial_uart = None

    def set_up_xbee_gateway(self):
        self._xbee = DigiMeshDevice("/dev/ttyS0", 9600)
        self._xbee.open()

    def set_up_message_queue(self):
        self._message_queue = Queue()

    def send_uart_messages(self):
        while True:
            command = self.message_queue.get()
            self.logger.info(f"Command: {command}")
            remote = RemoteXBeeDevice(self.xbee, XBee64BitAddress.from_hex_string(command.mac_id))
            remote.set_io_configuration(command.at_command, command.value)
            self.message_queue.task_done()
  
    def create_device_thread(self, device: DeviceModel):
        self.logger.debug(f"Creating thread for device: {device.device_id}")
        device_control = DeviceControl(device, self.message_queue, self.http_service, self.logger)
        self.device_map[device.device_id] = device
        self.device_control_map[device.device_id] = device_control
        device_control.start()

    def cleanup_devices(self):
        devices = list(self.device_map.values())
        for device in devices:
            if not device.alive:
                del self.device_map[device.device_id]
                self.device_control_map[device.device_id].stop_thread = True
                del self.device_control_map[device.device_id]

    def start_uart_sender(self):
        self.logger.info("Starting UART sender task!")
        Thread(target=self.send_uart_messages).start()

    def start_router_updater(self):
        self.logger.info("Starting router updater!")
        while True:
            time.sleep(20)
            updated_router = self.http_service.get_router_info()
            for device in updated_router["devices"]:
                device = DeviceModel(**device)
                if device.pins:
                    if device.device_id not in self.device_control_map.keys():
                        self.logger.debug("Device does not exist in device_control_map")
                        self.create_device_thread(device)    
                    elif not self.device_map[device.device_id] == device:
                        self.logger.debug(f"Updating device: {device.device_id}")
                        self.device_control_map[device.device_id].stop_thread = True
                        self.create_device_thread(device)
                    else:
                        self.logger.debug("Nothing happened")
                self.device_map[device.device_id].alive = True
            self.cleanup_devices()
                    
