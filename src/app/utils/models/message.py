from typing import Optional
from pydantic import BaseModel

from digi.xbee.io import IOValue, IOLine

class Command(BaseModel):
    mac_id: str
    at_command: IOLine
    value: IOValue