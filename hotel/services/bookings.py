from dataclasses import dataclass

from django.db.models import QuerySet

from hotel.models import Booking, Room
from hotel.serializers import BookingCreateSerializer


@dataclass
class BookingServiceError(Exception):
    message: str
    status_code: int


def create_booking(payload: dict) -> Booking:
    serializer = BookingCreateSerializer(data=payload)
    if not serializer.is_valid():
        raise BookingServiceError("Invalid dates", 400)

    room_id = serializer.validated_data["room_id"]
    date_start = serializer.validated_data["date_start"]
    date_end = serializer.validated_data["date_end"]

    if date_end < date_start:
        raise BookingServiceError("Invalid dates", 400)

    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist as exc:
        raise BookingServiceError("Room not found", 404) from exc

    return Booking.objects.create(room=room, date_start=date_start, date_end=date_end)


def delete_booking(booking_id: int) -> None:
    try:
        booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist as exc:
        raise BookingServiceError("Booking not found", 404) from exc
    booking.delete()


def list_bookings(room_id_raw: str | None) -> QuerySet[Booking]:
    if not room_id_raw:
        raise BookingServiceError("room_id is required", 400)
    try:
        room_id = int(room_id_raw)
    except ValueError as exc:
        raise BookingServiceError("room_id is required", 400) from exc

    if not Room.objects.filter(id=room_id).exists():
        raise BookingServiceError("Room not found", 404)

    return Booking.objects.filter(room_id=room_id).order_by("date_start")
