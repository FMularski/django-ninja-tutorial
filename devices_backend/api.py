from ninja import NinjaAPI

from core.api import router as core_router
from core.auth import ApiKeyAuth, KnoxAuth
from devices.api import router as devices_router
from rpg.api import router as rpg_router

api = NinjaAPI(auth=[ApiKeyAuth(), KnoxAuth()])  # apply global authentication

api.add_router("core/", core_router)
api.add_router("iot/", devices_router)
api.add_router("rpg/", rpg_router)
