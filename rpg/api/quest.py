from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import PageNumberPagination, paginate

from rpg.auth import ApiKey
from rpg.models import Quest
from rpg.schemas import QuestReadSchema, QuestWriteSchema

router = Router(auth=ApiKey(), tags=["Quests"])


@router.get("", response={HTTPStatus.OK: list[QuestReadSchema]})
@paginate(PageNumberPagination, page_size=5)
def get_quests(request):
    return HTTPStatus.OK, Quest.objects.all()


@router.get("{pk}/", response={HTTPStatus.OK: QuestReadSchema})
def get_quest(request, pk: int):
    return HTTPStatus.OK, get_object_or_404(Quest, pk=pk)


@router.post("", response={HTTPStatus.CREATED: QuestReadSchema})
def post_quest(request, quest: QuestWriteSchema):
    quest_data = quest.model_dump()
    return HTTPStatus.CREATED, Quest.objects.create(**quest_data)


@router.api_operation(["PUT", "PATCH"], "{pk}/", response={HTTPStatus.OK: QuestReadSchema})
def update_quest(request, pk: int, quest: QuestWriteSchema):
    existing_quest = get_object_or_404(Quest, pk=pk)
    quest_data = quest.model_dump()

    for k, v in quest_data.items():
        setattr(existing_quest, k, v)
    existing_quest.save()

    return HTTPStatus.OK, existing_quest


@router.delete("{pk}/", response={HTTPStatus.NO_CONTENT: None})
def delete_quest(request, pk: int):
    existing_quest = get_object_or_404(Quest, pk=pk)
    existing_quest.delete()

    return HTTPStatus.NO_CONTENT, None
