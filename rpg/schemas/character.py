from django.db.models import Q
from ninja import Field, FilterSchema, ModelSchema

from core.schemas import OrderSchema
from rpg import models

from .characterclass import CharacterClassReadSchema
from .quest import QuestReadSchema


class CharacterReadSchema(ModelSchema):
    character_class: CharacterClassReadSchema
    quests: list[QuestReadSchema]
    # TODO:
    # guild = schemas.GuildReadSchema
    # statistics = schemas.StatisticsReadSchema

    class Meta:
        model = models.Character
        fields = "__all__"


class CharacterOrderSchema(OrderSchema):
    pass


class CharacterFilterSchema(FilterSchema):
    character_class: str = Field(None, alias="class", q=["character_class__name__iexact"])
    name: str = Field(None, q=["name__icontains"])
    guild: str = Field(None, q=["guild__name__icontains"])
    gold: int = None
    level: int = None

    def filter_gold(self, gold):
        return Q(gold__gte=gold) if gold else Q()

    def filter_level(self, level):
        return Q(level__gte=level) if level else Q()
