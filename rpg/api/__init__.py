from ninja import Router

from .characterclass import router as character_class_router
from .item import router as items_router
from .quest import router as quests_router
from .rarity import router as rarities_router

router = Router()

router.add_router("classes/", character_class_router)
router.add_router("quests/", quests_router)
router.add_router("rarities/", rarities_router)
router.add_router("items/", items_router)
