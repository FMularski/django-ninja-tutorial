from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Router

from devices.models import Device, Location
from devices.schemas import DeviceSchema, DeviceWriteSchema, ErrorSchema

router = Router(tags=["Devices"])


@router.get("", response=list[DeviceSchema])
def get_devices(request):
    return Device.objects.all()


@router.get("{slug}/", response=DeviceSchema)
def get_device(request, slug: str):
    return get_object_or_404(Device, slug=slug)


@router.post("", response={HTTPStatus.CREATED: DeviceSchema, HTTPStatus.NOT_FOUND: ErrorSchema})
def post_device(request, device: DeviceWriteSchema):
    if device.location_id:
        location_exists = Location.objects.filter(pk=device.location_id).exists()
        if not location_exists:
            return HTTPStatus.NOT_FOUND, {"message": "Location not found."}

    device_data = device.model_dump()

    return HTTPStatus.CREATED, Device.objects.create(**device_data)


@router.put("{slug}/", response={HTTPStatus.OK: DeviceSchema, HTTPStatus.NOT_FOUND: ErrorSchema})
def put_device(request, slug: str, device: DeviceWriteSchema):
    existing_device = get_object_or_404(Device, slug=slug)

    if device.location_id:
        location_exists = Location.objects.filter(pk=device.location_id).exists()
        if not location_exists:
            return HTTPStatus.NOT_FOUND, {"message": "Location not found."}

    device_data = device.model_dump()
    existing_device.name = device_data.get("name")
    existing_device.location_id = device_data.get("location_id")
    existing_device.save()

    return existing_device
