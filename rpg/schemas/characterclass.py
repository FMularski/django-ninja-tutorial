from ninja import Field, ModelSchema
from pydantic import validator

from rpg import models


class CharacterClassReadSchema(ModelSchema):
    class Meta:
        model = models.CharacterClass
        fields = "__all__"


class CharacterClassWriteSchema(ModelSchema):
    name: str = Field(default="Default class")
    description: str = Field(default="Default description")

    class Meta:
        model = models.CharacterClass
        fields = (
            "name",
            "description",
        )

    @validator("description")
    def description_length_must_be_even(cls, description):
        if len(description) % 2:
            raise ValueError("The length of the description must be an even number")
        return description
