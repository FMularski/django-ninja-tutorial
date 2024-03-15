from http import HTTPStatus

from ninja import Query, Router
from ninja.pagination import PageNumberPagination, paginate

from rpg.models import Item
from rpg.schemas import ItemFilterSchema, ItemOrderSchema, ItemReadSchema

router = Router(tags=["Items"])


@router.get("", response={HTTPStatus.OK: list[ItemReadSchema]})
@paginate(PageNumberPagination, page_size=10)
def get_items(request, filters: ItemFilterSchema = Query(), ordering: ItemOrderSchema = Query()):
    items = Item.objects.all()
    filtered = filters.filter(items)
    ordered = ordering.order(filtered)

    return ordered
