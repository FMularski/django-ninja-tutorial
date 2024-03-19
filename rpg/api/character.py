from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Query, Router
from ninja.pagination import PageNumberPagination, paginate

from rpg.models import Character, CharacterClass, Guild, Statistics
from rpg.schemas import (
    CharacterFilterSchema,
    CharacterOrderSchema,
    CharacterReadSchema,
    CharacterWriteSchema,
)

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


@router.post("", response={HTTPStatus.CREATED: CharacterReadSchema})
def post_character(request, character: CharacterWriteSchema):
    character_class = get_object_or_404(CharacterClass, pk=character.character_class)
    guild = get_object_or_404(Guild, pk=character.guild)

    statistics_data = character.statistics.model_dump()
    statistics = Statistics.objects.create(
        **statistics_data,
        base_max_health=statistics_data["base_health"],
        base_max_mana=statistics_data["base_mana"]
    )

    return HTTPStatus.CREATED, Character.objects.create(
        name=character.name,
        character_class=character_class,
        guild=guild,
        statistics=statistics,
    )


@router.delete("{pk}/", response={HTTPStatus.NO_CONTENT: None})
def delete_character(request, pk: int):
    existing_character = get_object_or_404(Character, pk=pk)
    existing_character.delete()

    return HTTPStatus.NO_CONTENT, None
