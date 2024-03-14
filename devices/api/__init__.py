from ninja import Router

from .device import router as devices_router
from .location import router as locations_router

router = Router()

router.add_router("locations/", locations_router)
router.add_router("devices/", devices_router)
