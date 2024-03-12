from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import PageNumberPagination, paginate

from rpg.auth import ApiKey
from rpg.models import CharacterClass
from rpg.schemas import CharacterClassReadSchema, CharacterClassWriteSchema

router = Router(auth=ApiKey(), tags=["Character classes"])


@router.get("", response={HTTPStatus.OK: list[CharacterClassReadSchema]})
@paginate(PageNumberPagination, page_size=3)
def get_classes(request):
    return HTTPStatus.OK, CharacterClass.objects.all()


@router.post("", response={HTTPStatus.CREATED: CharacterClassReadSchema})
def post_class(request, class_: CharacterClassWriteSchema):
    class_data = class_.model_dump()
    return HTTPStatus.CREATED, CharacterClass.objects.create(**class_data)


@router.api_operation(
    ["PUT", "PATCH"], "{pk}/", response={HTTPStatus.OK: CharacterClassReadSchema}
)
def update_class(request, pk: int, class_: CharacterClassWriteSchema):
    existing_class = get_object_or_404(CharacterClass, pk=pk)
    existing_class.name = class_.name
    existing_class.description = class_.description
    existing_class.save()

    return existing_class


@router.delete("{pk}/", response={HTTPStatus.NO_CONTENT: None})
def delete_class(request, pk: int):
    existing_class = get_object_or_404(CharacterClass, pk=pk)
    existing_class.delete()

    return HTTPStatus.NO_CONTENT, None
