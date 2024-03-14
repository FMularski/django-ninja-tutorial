from ninja import ModelSchema, Schema

from devices import models
from devices.schemas.location import LocationSchema


class DeviceSchema(ModelSchema):
    location: LocationSchema | None = None

    class Meta:
        model = models.Device
        fields = ("id", "name", "slug", "location")


class DeviceWriteSchema(Schema):
    name: str
    location_id: int | None = None
