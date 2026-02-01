from django.db.models import QuerySet

from hotel.models import Booking, Room
from hotel.serializers import BookingCreateSerializer

from .exceptions import BookingServiceError


def create_booking(payload: dict) -> Booking:
    serializer = BookingCreateSerializer(data=payload)
    if not serializer.is_valid():
        raise BookingServiceError("Invalid dates", 400)

    room_id = serializer.validated_data["room_id"]
    date_start = serializer.validated_data["date_start"]
    date_end = serializer.validated_data["date_end"]

    if date_end < date_start:
        raise BookingServiceError("Invalid dates", 400)

    room = Room.objects.filter(id=room_id).first()
    if room is None:
        raise BookingServiceError("Room not found", 404)

    return Booking.objects.create(room=room, date_start=date_start, date_end=date_end)


def delete_booking(booking_id: int) -> None:
    booking = Booking.objects.filter(pk=booking_id).first()
    if booking is None:
        raise BookingServiceError("Booking not found", 404)
    booking.delete()


def list_bookings(room_id_raw: str | None) -> QuerySet[Booking]:
    if not room_id_raw:
        raise BookingServiceError("room_id is required", 400)
    room_id_text = room_id_raw.strip()
    if not room_id_text.isdigit():
        raise BookingServiceError("room_id is required", 400)
    room_id = int(room_id_text)

    if not Room.objects.filter(id=room_id).exists():
        raise BookingServiceError("Room not found", 404)

    return Booking.objects.filter(room_id=room_id).order_by("date_start")
