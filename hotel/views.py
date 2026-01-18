from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import BookingListSerializer, RoomListSerializer
from .services import BookingServiceError, RoomServiceError
from .services.bookings import (
    create_booking as create_booking_service,
    delete_booking as delete_booking_service,
    list_bookings as list_bookings_service,
)
from .services.rooms import (
    create_room as create_room_service,
    delete_room as delete_room_service,
    list_rooms as list_rooms_service,
)


@api_view(["POST"])
def create_room(request):
    try:
        room = create_room_service(request.data)
    except RoomServiceError as exc:
        return Response({"error": exc.message}, status=exc.status_code)
    return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_room(request, room_id: int):
    try:
        delete_room_service(room_id)
    except RoomServiceError as exc:
        return Response({"error": exc.message}, status=exc.status_code)
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def list_rooms(request):
    try:
        rooms = list_rooms_service(
            request.query_params.get("sort"),
            request.query_params.get("order"),
        )
    except RoomServiceError as exc:
        return Response({"error": exc.message}, status=exc.status_code)
    serializer = RoomListSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_booking(request):
    try:
        booking = create_booking_service(request.data)
    except BookingServiceError as exc:
        return Response({"error": exc.message}, status=exc.status_code)
    return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_booking(request, booking_id: int):
    try:
        delete_booking_service(booking_id)
    except BookingServiceError as exc:
        return Response({"error": exc.message}, status=exc.status_code)
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def list_bookings(request):
    try:
        bookings = list_bookings_service(request.query_params.get("room_id"))
    except BookingServiceError as exc:
        return Response({"error": exc.message}, status=exc.status_code)
    serializer = BookingListSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
