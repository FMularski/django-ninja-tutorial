from http import HTTPStatus

from django.db.models import F, Value
from django.db.models.functions import Length, StrIndex, Substr
from django.shortcuts import get_object_or_404
from ninja import File, Query, Router
from ninja.files import UploadedFile
from ninja.pagination import PageNumberPagination, paginate

from rpg.models import Guild
from rpg.schemas import GuildFilterSchema, GuildOrderSchema, GuildReadSchema, GuildWriteSchema

router = Router(tags=["Guilds"])


@router.get("", response={HTTPStatus.OK: list[GuildReadSchema]})
@paginate(PageNumberPagination, page_size=10)
def get_guilds(
    request, ordering: GuildOrderSchema = Query(), filters: GuildFilterSchema = Query()
):
    guilds = Guild.objects.all().annotate(
        banner_ext=Substr(
            F("banner"),
            StrIndex(F("banner"), Value(".")) + 1,
            Length(F("banner")) - StrIndex(F("banner"), Value(".")),
        )
    )
    filtered = filters.filter(guilds)
    ordered = ordering.order(filtered)

    return HTTPStatus.OK, ordered


@router.get("{pk}/", response={HTTPStatus.OK: GuildReadSchema})
def get_guild(request, pk: int):
    return HTTPStatus.OK, get_object_or_404(Guild, pk=pk)


@router.post("", response={HTTPStatus.CREATED: GuildReadSchema})
def post_guild(request, guild: GuildWriteSchema, banner: UploadedFile = File()):
    guild_data = guild.model_dump()
    return HTTPStatus.CREATED, Guild.objects.create(**guild_data, banner=banner)


@router.api_operation(["PUT", "PATCH"], "{pk}/", response={HTTPStatus.OK: GuildReadSchema})
def update_guild(request, pk: int, guild: GuildWriteSchema, banner: UploadedFile = File(None)):
    existing_guild = get_object_or_404(Guild, pk=pk)
    guild_data = guild.model_dump()

    for k, v in guild_data.items():
        setattr(existing_guild, k, v)

    if banner:
        existing_guild.banner = banner

    existing_guild.save()
    return HTTPStatus.OK, existing_guild


@router.delete("{pk}/", response={HTTPStatus.NO_CONTENT: None})
def delete_guild(request, pk: int):
    existing_guild = get_object_or_404(Guild, pk=pk)
    existing_guild.delete()

    return HTTPStatus.NO_CONTENT, None
