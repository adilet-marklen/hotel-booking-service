from dataclasses import dataclass

from django.db.models import QuerySet

from hotel.models import Room
from hotel.serializers import RoomCreateSerializer


@dataclass
class RoomServiceError(Exception):
    message: str
    status_code: int


def create_room(payload: dict) -> Room:
    serializer = RoomCreateSerializer(data=payload)
    if not serializer.is_valid():
        raise RoomServiceError("Invalid payload", 400)
    return serializer.save()


def delete_room(room_id: int) -> None:
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist as exc:
        raise RoomServiceError("Room not found", 404) from exc
    room.delete()


def list_rooms(sort: str | None, order: str | None) -> QuerySet[Room]:
    sort_value = sort or "created_at"
    order_value = order or "asc"

    valid_sorts = {"price", "created_at"}
    valid_orders = {"asc", "desc"}
    if sort_value not in valid_sorts or order_value not in valid_orders:
        raise RoomServiceError("Invalid sort or order", 400)

    ordering = sort_value if order_value == "asc" else f"-{sort_value}"
    return Room.objects.all().order_by(ordering)
