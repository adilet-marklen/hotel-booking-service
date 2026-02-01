from rest_framework import serializers

from .models import Booking, Room


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["description", "price"]


class RoomListSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Room
        fields = ["room_id", "description", "price", "created_at"]


class BookingCreateSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ["room_id", "date_start", "date_end"]


class BookingListSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Booking
        fields = ["booking_id", "date_start", "date_end"]
