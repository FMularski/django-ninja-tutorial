from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Query, Router

from core.auth import KnoxAuth
from rpg.models import Rarity
from rpg.schemas import RarityFilterSchema, RarityReadSchema, RarityWriteSchema

router = Router(auth=KnoxAuth(), tags=["Rarities"])


@router.get("", response={HTTPStatus.OK: list[RarityReadSchema]})
def get_rarities(request, filters: RarityFilterSchema = Query()):
    rarities = Rarity.objects.all()
    return HTTPStatus.OK, filters.filter(rarities)


@router.get("{pk}/", response={HTTPStatus.OK: RarityReadSchema})
def get_rarity(request, pk: int):
    return HTTPStatus.OK, get_object_or_404(Rarity, pk=pk)


@router.post("", response={HTTPStatus.CREATED: RarityReadSchema})
def post_rarity(request, rarity: RarityWriteSchema):
    rarity_data = rarity.model_dump()
    return HTTPStatus.CREATED, Rarity.objects.create(**rarity_data)


@router.api_operation(["PUT", "PATCH"], "{pk}/", response={HTTPStatus.OK: RarityReadSchema})
def update_rarity(request, pk: int, rarity: RarityWriteSchema):
    existing_rarity = get_object_or_404(Rarity, pk=pk)
    rarity_data = rarity.model_dump()

    for k, v in rarity_data.items():
        setattr(existing_rarity, k, v)
    existing_rarity.save()

    return HTTPStatus.OK, existing_rarity


@router.delete("{pk}/", response={HTTPStatus.NO_CONTENT: None})
def delete_rarity(request, pk: int):
    existing_rarity = get_object_or_404(Rarity, pk=pk)
    existing_rarity.delete()

    return HTTPStatus.NO_CONTENT, None
