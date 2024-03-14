import re

from django.db.models import Q
from ninja import Field, FilterSchema, ModelSchema
from pydantic import validator

from rpg import models


class RarityReadSchema(ModelSchema):
    class Meta:
        model = models.Rarity
        fields = "__all__"


class RarityWriteSchema(ModelSchema):
    color: str  # required to declate here to apply validator
    grade: int  # required to declate here to apply validator

    class Meta:
        model = models.Rarity
        fields = (
            "name",
            "color",
            "grade",
        )

    @validator("color")
    def color_must_be_a_valid_hex(cls, color):
        hex_pattern = r"^#(?:[0-9a-fA-F]{3}){1,2}$"
        if not re.match(hex_pattern, color):
            raise ValueError("Invalid hex code.")

        return color

    @validator("grade")
    def grade_must_be_positive(cls, grade):
        if grade < 1:
            raise ValueError("Invalid grade.")

        return grade


class RarityFilterSchema(FilterSchema):
    name: str = Field(
        None, alias="title", q=["name__icontains"]
    )  # Field(...) means that the "name" param is required, alias renames the param
    color: str = Field(None, pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$")  #
    min_grade: int = Field(None, q=["grade__gte"])
    premium: bool | None = None

    def filter_premium(self, premium: bool) -> Q:  # a custom filter, filter_<field_name>
        return Q(grade__gte=3) if premium else Q()
