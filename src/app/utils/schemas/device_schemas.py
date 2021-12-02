from marshmallow import Schema, fields

class CronPeriodsSchema(Schema):
    cron_id = fields.Int(data_key="cronID")
    start_offset = fields.Int(data_key="startOffset")
    time_on = fields.Int(data_key="timeOn")
    time_off = fields.Int(data_key="timeOff")


class PinTypeSchema(Schema):
    type_id = fields.Int(data_key="typeID")
    name = fields.Str()


class DeviceTypeSchema(Schema):
    type_id = fields.Int(data_key="typeID")
    name = fields.Str()


class DevicePinSchema(Schema):
    pin_id = fields.Int(data_key="pinID")
    device_id = fields.Int(data_key="deviceID")
    description = fields.Str()
    type_id = fields.Int(data_key="typeID")
    value = fields.Int()
    device_pin_id = fields.Str(data_key="devicePinID")
    cron_id = fields.Int(data_key="cronID", allow_none=True)
    type = fields.Nested(PinTypeSchema)
    cron = fields.Nested(CronPeriodsSchema, allow_none=True)


class DeviceSchema(Schema):
    device_id = fields.Int(data_key="deviceID")
    mac_id = fields.Str(data_key="macID", required=True)
    description = fields.Str()
    type_id = fields.Int(data_key="typeID")
    router_id = fields.Str(data_key="routerID")
    pins = fields.List(fields.Nested(DevicePinSchema))
    type = fields.Nested(DeviceTypeSchema)


class DeviceListSchema(Schema):
    devices = fields.List(fields.Nested(DeviceSchema))


class DevicePinValueSchema(Schema):
    pin_id = fields.Int(data_key="pinID")
    value = fields.Int()


class UpdateDevicePinSchema(Schema):
    pins = fields.List(fields.Nested(DevicePinValueSchema))

