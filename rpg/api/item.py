from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import File, Query, Router
from ninja.files import UploadedFile
from ninja.pagination import PageNumberPagination, paginate

from rpg.models import Item
from rpg.schemas import ItemFilterSchema, ItemOrderSchema, ItemReadSchema, ItemWriteSchema

router = Router(tags=["Items"])


@router.get("", response={HTTPStatus.OK: list[ItemReadSchema]})
@paginate(PageNumberPagination, page_size=10)
def get_items(request, filters: ItemFilterSchema = Query(), ordering: ItemOrderSchema = Query()):
    items = Item.objects.all()
    filtered = filters.filter(items)
    ordered = ordering.order(filtered)

    return ordered


@router.get("{pk}/", response={HTTPStatus.OK: ItemReadSchema})
def get_item(request, pk: int):
    return get_object_or_404(Item, pk=pk)


@router.post("", response={HTTPStatus.CREATED: ItemReadSchema})
def post_item(request, item: ItemWriteSchema, icon: UploadedFile = File(None)):
    item_data = item.model_dump()
    return Item.objects.create(**item_data, icon=icon)
