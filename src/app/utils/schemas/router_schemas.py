from marshmallow import Schema, fields

from app.utils.schemas.device_schemas import DeviceSchema

class RouterSchema(Schema):
    router_id = fields.Int(data_key="routerID")
    description = fields.Str()
    latitude = fields.Str()
    longitude = fields.Str()
    devices = fields.List(fields.Nested(DeviceSchema))

class RouterListSchema(Schema):
    routers = fields.List(fields.Nested(RouterSchema))