from django.urls import path

from . import views

urlpatterns = [
    path("rooms/create", views.create_room, name="rooms-create"),
    path("rooms", views.list_rooms, name="rooms-list"),
    path("rooms/<int:room_id>", views.delete_room, name="rooms-delete"),
    path("bookings/create", views.create_booking, name="bookings-create"),
    path("bookings/list", views.list_bookings, name="bookings-list"),
    path("bookings/<int:booking_id>", views.delete_booking, name="bookings-delete"),
]
