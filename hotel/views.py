from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import BookingListSerializer, RoomListSerializer
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
    room = create_room_service(request.data)
    return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_room(request, room_id: int):
    delete_room_service(room_id)
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def list_rooms(request):
    rooms = list_rooms_service(
        request.query_params.get("sort"),
        request.query_params.get("order"),
    )
    serializer = RoomListSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_booking(request):
    booking = create_booking_service(request.data)
    return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_booking(request, booking_id: int):
    delete_booking_service(booking_id)
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def list_bookings(request):
    bookings = list_bookings_service(request.query_params.get("room_id"))
    serializer = BookingListSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
