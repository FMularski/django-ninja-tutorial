from django.db.models import Q
from ninja import Field, FilterSchema, ModelSchema

from core.schemas import OrderSchema
from rpg import models


class ItemReadSchema(ModelSchema):
    class Meta:
        model = models.Item
        fields = "__all__"


class ItemFilterSchema(FilterSchema):
    name: str = Field(None, q=["name__icontains"])
    rarity: str = Field(None, q=["rarity__name__iexact"], description="Rarity name, ex. Epic")
    stat: str = Field(None, q=["boosted_stat__iexact"])
    min_value: int = Field(None, q=["value__gte"])
    melee: bool | None = None
    magic: bool | None = None

    # filter items recommended for melee classes
    def filter_melee(self, melee: bool):
        return Q(boosted_stat__in=["strength", "health"]) if melee else Q()

    # filter items recommeded for magic classes
    def filter_magic(self, magic: bool):
        return Q(boosted_stat__in=["intelligence", "mana"]) if magic else Q()


class ItemOrderSchema(OrderSchema):
    pass
