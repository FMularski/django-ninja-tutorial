from ninja import NinjaAPI

from .characterclass import router as character_class_router
from .quest import quest_api

api = NinjaAPI(urls_namespace="rpg")

api.add_router("classes/", character_class_router)
api.add_router("quests/", quest_api.router)
