from pydantic import BaseModel
from typing import List

from app.utils.models.device import DeviceModel

class RouterModel(BaseModel):
    class Config:
       orm_mode = True 

    router_id: int
    latitude: str
    longitude: str
    description: str
    devices: List[DeviceModel]
    