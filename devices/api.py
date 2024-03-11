from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from devices.models import Device, Location
from devices.schemas import DeviceSchema, LocationSchema

api = NinjaAPI()


@api.get("devices/", response=list[DeviceSchema])
def get_devices(request):
    return Device.objects.all()


@api.get("devices/{slug}/", response=DeviceSchema)
def get_device(request, slug: str):
    return get_object_or_404(Device, slug=slug)


@api.get("locations/", response=list[LocationSchema])
def get_devices(request):
    return Location.objects.all()
