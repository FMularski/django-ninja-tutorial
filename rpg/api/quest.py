from http import HTTPStatus

from ninja import Router

from rpg.auth import ApiKey
from rpg.models import Quest
from rpg.schemas import QuestReadSchema


class QuestAPI:
    def __init__(self):
        self.router = Router(auth=ApiKey(), tags=["Quests"])
        self.register_routes()

    def register_routes(self):
        @self.router.get("", response={HTTPStatus.OK: list[QuestReadSchema]})
        def get_quests(request):
            return Quest.objects.all()


quest_api = QuestAPI()
