from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Query, Router
from ninja.pagination import PageNumberPagination, paginate

from rpg.models import Character
from rpg.schemas import CharacterFilterSchema, CharacterOrderSchema, CharacterReadSchema

router = Router(tags=["Characters"])


@router.get("", response={HTTPStatus.OK: list[CharacterReadSchema]})
@paginate(PageNumberPagination, page_size=5)
def get_characters(
    request, ordering: CharacterOrderSchema = Query(), filters: CharacterFilterSchema = Query()
):
    characters = Character.objects.all()
    filtered = filters.filter(characters)
    ordered = ordering.order(filtered)

    return HTTPStatus.OK, ordered


@router.get("{pk}/", response={HTTPStatus.OK: CharacterReadSchema})
def get_character(request, pk: int):
    return HTTPStatus.OK, get_object_or_404(Character, pk=pk)


@router.delete("{pk}/", response={HTTPStatus.NO_CONTENT: None})
def delete_character(request, pk: int):
    existing_character = get_object_or_404(Character, pk=pk)
    existing_character.delete()

    return HTTPStatus.NO_CONTENT, None
