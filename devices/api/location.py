from http import HTTPStatus

from ninja import Router

from devices.models import Location
from devices.schemas import LocationSchema

router = Router(tags=["Locations"])


@router.get("", response={HTTPStatus.OK: list[LocationSchema]})
def get_locations(request):
    return Location.objects.all()
