from logging import Logger
import time
from datetime import datetime
from queue import Queue
from threading import Thread, get_ident

from app.utils.models.device import DeviceModel, PinType, DevicePinModel
from app.utils.models.message import Command
from app.services.http import HTTPService
from app.utils.logger import configure_logger


class DeviceControl:

    def __init__(
        self,
        device: DeviceModel,
        message_queue: Queue,
        http_service: HTTPService,
        logger: Logger
    ):
        self._device = device
        self._message_queue= message_queue
        self.logger = logger
        self.http_service = http_service
        self._stop_thread = False

    @property
    def message_queue(self):
        return self._message_queue

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value: DeviceModel):
        self._device = value

    @property
    def stop_thread(self):
        return self._stop_thread

    @stop_thread.setter
    def stop_thread(self, value: bool):
        self._stop_thread = value

    def start(self):
        device_thread = Thread(target=self.check_device_status)
        device_thread.start()
        return device_thread

    def check_device_status(self):
        self.logger.info("Started thread!")
        while True:
            if self.stop_thread:
                break
            if len(self.device.pins_updated)<len(self.device.pins):
                self.update_device_output()
            self.device.alive = False
            time.sleep(5) 

    def update_device_output(self):
        cron_updated_pins = []
        for pin in self.device.pins:
            if pin.type_id == PinType.OUTPUT.value and not (pin.pin_id in self.device.pins_updated):
                if pin.cron_id is not None:
                    new_value = self.get_cron_output_value(pin)
                    if new_value == pin.value:
                        continue
                    else:
                        pin.value = new_value
                        cron_updated_pins.append(
                            {
                                "pin_id": pin.pin_id,
                                "value": pin.value
                            }
                        )
                else:
                    self.device.pins_updated.append(pin.pin_id)
                command = Command(**{
                    "mac_id": self.device.mac_id,
                    "at_command": pin.io_line,
                    "value": pin.xbee_value
                })
                self.send_command(command)
        if len(cron_updated_pins) > 0:
            self.http_service.update_device_pin_values(
                device_id=self.device.device_id,
                updated_device={
                    "pins": cron_updated_pins
                }
            )

    def send_command(self, command: Command):
        self.message_queue.put(command)

    @staticmethod
    def seconds_from_midnight() -> int:
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return (now - midnight).seconds

    @classmethod               
    def get_cron_output_value(cls, pin: DevicePinModel) -> int:
        seconds_from_mn = cls.seconds_from_midnight()
        period_percentage = (seconds_from_mn + pin.cron.start_offset) % pin.cron.period
        if period_percentage < pin.cron.time_on:
            output = 1
        else:
            output = 0
        return output