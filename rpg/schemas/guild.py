from django.db.models import Q
from ninja import Field, FilterSchema, ModelSchema, Schema

from core.schemas import OrderSchema
from rpg import models


class BannerDetailSchema(Schema):
    filename: str
    ext: str
    size: int
    url: str


class GuildReadSchema(ModelSchema):
    banner: BannerDetailSchema

    class Meta:
        model = models.Guild
        fields = "__all__"

    @staticmethod
    def resolve_banner(obj):
        return BannerDetailSchema.model_validate(
            {
                "filename": obj.banner.name.split("/")[-1],
                "ext": obj.banner_ext,
                "size": obj.banner.size,
                "url": obj.banner.url,
            }
        )


class GuildOrderSchema(OrderSchema):
    pass


class GuildFilterSchema(FilterSchema):
    name: str = Field(None, q="name__icontains")
    banner_ext: str = None

    def filter_banner_ext(cls, banner_ext: str) -> Q:
        return Q(banner_ext__iexact=banner_ext) if banner_ext else Q()
