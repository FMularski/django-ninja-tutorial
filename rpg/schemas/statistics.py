from ninja import ModelSchema

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
        fields = "__all__"
