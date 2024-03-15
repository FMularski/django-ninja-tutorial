from django.db.models import Q
from ninja import Field, FilterSchema, ModelSchema, Schema
from pydantic import validator

from core.schemas import OrderSchema
from rpg import models


class ItemReadSchema(ModelSchema):
    recommended: str

    class Meta:
        model = models.Item
        fields = "__all__"

    @staticmethod
    def resolve_recommended(obj, context):
        """
        * resolver is the equivalent of SerializerMethodField
        * context can be accessed here
        * serializing object outside request and passing custom context:
            DRF:
            serializer = SerializerClass(instance, context={...})
            serializer.data

            django-ninja:
            schema = SchemaClass.from_orm(instance, context={...})
            schema.dict()
        """
        auth = context["request"].auth

        recommended = ""
        if obj.boosted_stat in ["health", "strength"]:
            recommended = "melee"
        elif obj.boosted_stat in ["mana", "intelligence"]:
            recommended = "magic"
        else:
            recommended = "rogue"

        return f"{auth} - {recommended}"


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


class ItemWriteSchema(Schema):
    name: str
    rarity: str
    boosted_stat: str
    value: int = Field(gt=0)
    character_id: int

    class Meta:
        model = models.Item
        exclude = (
            "id",
            "icon",
        )  # icon must be handled separately

    @validator("rarity")
    def check_if_rarity_exists(cls, rarity: str):
        # input: rarity name (str)
        # output: rarity object
        rarity_obj = models.Rarity.objects.filter(name__iexact=rarity).first()
        if not rarity_obj:
            raise ValueError("Invalid rarity.")

        return rarity_obj

    @validator("boosted_stat")
    def check_boosted_stat(cls, boosted_stat: str):
        available_stats = ["health", "mana", "strength", "intelligence", "agility"]
        if boosted_stat not in available_stats:
            raise ValueError(f"Invalid boosted stat, choices are: {', '.join(available_stats)}.")

        return boosted_stat

    @validator("character_id")
    def check_if_character_exists(cls, character_id: int):
        if not models.Character.objects.filter(pk=character_id).exists():
            raise ValueError("Invalid character.")

        return character_id
