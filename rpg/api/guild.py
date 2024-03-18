from http import HTTPStatus

from django.db.models import F, Value
from django.db.models.functions import Length, StrIndex, Substr
from ninja import Query, Router
from ninja.pagination import PageNumberPagination, paginate

from rpg.models import Guild
from rpg.schemas import GuildFilterSchema, GuildOrderSchema, GuildReadSchema

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

    return ordered
