import enum
from typing import List, Optional

from pydantic import BaseModel
from dictdiffer import diff
from digi.xbee.io import IOLine, IOValue

pin_type_io_line_map = {io_line.at_command:io_line for io_line in IOLine}


class PinType(enum.Enum):
    OUTPUT = 1
    INPUT = 2


class PinTypeModel(BaseModel):
    type_id: int
    name: str
    description: Optional[str]


class CronPeriodModel(BaseModel):
    cron_id: int
    start_offset: int
    time_on: int
    time_off: int

    @property
    def period(self):
        return self.time_on + self.time_off


class DevicePinModel(BaseModel):
    pin_id: int
    device_id: int
    type_id: int
    description: Optional[str]
    device_pin_id: str
    value: Optional[int] = 0
    cron_id: Optional[int] = None
    type: PinTypeModel
    cron: Optional[CronPeriodModel] = None

    @property
    def xbee_value(self):
        return IOValue.HIGH if self.value else IOValue.LOW

    @property
    def io_line(self) -> IOLine:
        return pin_type_io_line_map.get(self.device_pin_id, None)


class DeviceTypeModel(BaseModel):
    type_id: int
    name: str
    description: Optional[str]


class DeviceModel(BaseModel):
    device_id: int
    mac_id: str
    type_id: int
    description: Optional[str]
    router_id: int
    pins: List[DevicePinModel]
    type: DeviceTypeModel
    alive: Optional[bool] = True
    pins_updated: Optional[List[int]] = []

    def __eq__(self, other):
        return len(list(diff(self.dict(), other.dict(), ignore=["alive", "pins_updated"]))) == 0

