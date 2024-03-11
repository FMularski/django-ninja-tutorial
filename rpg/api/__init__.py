from ninja import NinjaAPI

from .characterclass import router as character_class_router

api = NinjaAPI(urls_namespace="rpg")

api.add_router("classes/", character_class_router)
