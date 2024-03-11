from ninja import ModelSchema

from devices import models


class LocationSchema(ModelSchema):
    class Meta:
        model = models.Location
        fields = ("id", "name")


class DeviceSchema(ModelSchema):
    location: LocationSchema | None = None

    class Meta:
        model = models.Device
        fields = ("id", "name", "slug", "location")
