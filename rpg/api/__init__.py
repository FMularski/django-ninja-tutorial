from ninja import NinjaAPI

from .characterclass import router as character_class_router
from .quest import router as quests_router
from .rarity import router as rarities_router

api = NinjaAPI(urls_namespace="rpg")

api.add_router("classes/", character_class_router)
api.add_router("quests/", quests_router)
api.add_router("rarities/", rarities_router)
