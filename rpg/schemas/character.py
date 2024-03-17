from ninja import ModelSchema, FilterSchema, Field
from rpg import models, schemas
from core.schemas import OrderSchema
from django.db.models import Q


class CharacterReadSchema(ModelSchema):
    character_class: schemas.CharacterClassReadSchema
    quests: list[schemas.QuestReadSchema]
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