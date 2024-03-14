from http import HTTPStatus

from ninja import Query, Router
from ninja.pagination import PageNumberPagination, paginate

from rpg.models import Item
from rpg.schemas import ItemFilterSchema, ItemReadSchema

router = Router(tags=["Items"])


@router.get("", response={HTTPStatus.OK: list[ItemReadSchema]})
@paginate(PageNumberPagination, page_size=10)
def get_items(request, filters: ItemFilterSchema = Query()):
    items = Item.objects.all()
    return filters.filter(items)
