from ninja import Field, ModelSchema, Schema
from pydantic import model_validator

from rpg import models


class StatisticsReadSchema(ModelSchema):
    # these are read from model properties
    health: int
    max_health: int
    mana: int
    max_mana: int
    strength: int
    intelligence: int
    agility: int
    is_dead: bool

    class Meta:
        model = models.Statistics
        exclude = ("id",)


class StatisticsWriteSchema(Schema):
    base_health: int = Field(default=100, ge=100)
    base_mana: int = Field(default=100, ge=100)
    base_strength: int = Field(default=10, ge=10)
    base_intelligence: int = Field(default=10, ge=10)
    base_agility: int = Field(default=10, ge=10)

    @model_validator(
        mode="after"
    )  # object-level validator (mode="after" -> after built-in pydantics validations)
    def check_sum_of_stats(self):
        spendable_limit = 10
        default_limit = 50

        if (
            self.base_health / 10
            + self.base_mana / 10
            + self.base_strength
            + self.base_intelligence
            + self.base_agility
            != default_limit + spendable_limit
        ):
            raise ValueError("Exactly 10 statistics points must be spend.")

        return self

    @model_validator(
        mode="before"
    )  # object-level validator (mode="before" -> before built-in pydantics validations)
    @classmethod  # must be a class method
    def check_something_else(cls, data):
        # ...
        return data
