from ninja import ModelSchema

from devices import models


class LocationSchema(ModelSchema):
    class Meta:
        model = models.Location
        fields = ("id", "name")
