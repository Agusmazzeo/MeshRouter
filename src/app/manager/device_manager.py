import time
from datetime import datetime
from queue import Queue
from threading import Thread
from typing import Dict

from app.utils.models.device import DeviceModel, PinType, DevicePinModel
from app.utils.models.message import Command
from app.utils.logger import configure_logger


class DeviceControl:

    def __init__(self, device: DeviceModel, message_queue: Queue):
        self._device = device
        self._message_queue= message_queue
        self.logger = configure_logger(f"Device {device.device_id}")
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
        while True:
            if self.stop_thread:
                break
            self.update_device_output()
            time.sleep(5) 

    def update_device_output(self):
        for pin in self.device.pins:
            if pin.type_id == PinType.OUTPUT.value:
                if pin.cron_id:
                    new_value = self.get_cron_output_value(pin)
                    if new_value == pin.value:
                        continue
                    else:
                        pin.value = new_value
                command = Command(**{
                    "mac_id": self.device.mac_id,
                    "at_command": pin.io_line,
                    "value": pin.xbee_value
                })
                self.send_command(command)

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