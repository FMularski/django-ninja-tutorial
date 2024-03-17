from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination
from http import HTTPStatus
from rpg.models import Character
from rpg.schemas import CharacterReadSchema, CharacterOrderSchema, CharacterFilterSchema

router = Router(tags=["Characters"])


@router.get("", response={HTTPStatus.OK: list[CharacterReadSchema]})
@paginate(PageNumberPagination, page_size=5)
def get_characters(request, ordering: CharacterOrderSchema = Query(), filters: CharacterFilterSchema = Query()):
    characters = Character.objects.all()
    filtered = filters.filter(characters)
    ordered = ordering.order(filtered)

    return ordered