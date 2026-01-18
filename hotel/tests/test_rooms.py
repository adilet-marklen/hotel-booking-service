import datetime as dt

import pytest
from django.urls import reverse
from django.utils import timezone

from hotel.models import Booking, Room


@pytest.mark.django_db
def test_create_room(api_client):
    url = reverse("rooms-create")
    response = api_client.post(
        url, {"description": "Cozy", "price": 1200}, format="json"
    )

    assert response.status_code == 201
    assert "room_id" in response.data
    assert Room.objects.count() == 1


@pytest.mark.django_db
def test_delete_room_cascades_bookings(api_client, room):
    Booking.objects.create(
        room=room, date_start=dt.date(2021, 12, 30), date_end=dt.date(2022, 1, 2)
    )

    url = reverse("rooms-delete", kwargs={"room_id": room.id})
    response = api_client.delete(url)

    assert response.status_code == 200
    assert Room.objects.count() == 0
    assert Booking.objects.count() == 0


@pytest.mark.django_db
def test_list_rooms_sort_price(api_client):
    Room.objects.create(description="Cheap", price=500)
    Room.objects.create(description="Expensive", price=2000)

    url = reverse("rooms-list")

    response = api_client.get(url, {"sort": "price", "order": "asc"})
    assert response.status_code == 200
    assert [r["price"] for r in response.data] == [500, 2000]

    response = api_client.get(url, {"sort": "price", "order": "desc"})
    assert response.status_code == 200
    assert [r["price"] for r in response.data] == [2000, 500]


@pytest.mark.django_db
def test_list_rooms_sort_created_at(api_client):
    older = Room.objects.create(description="Old", price=1000)
    newer = Room.objects.create(description="New", price=1100)

    base_time = timezone.now()
    Room.objects.filter(pk=older.pk).update(created_at=base_time - dt.timedelta(days=1))
    Room.objects.filter(pk=newer.pk).update(created_at=base_time)

    url = reverse("rooms-list")

    response = api_client.get(url, {"sort": "created_at", "order": "asc"})
    assert response.status_code == 200
    assert [r["room_id"] for r in response.data] == [older.id, newer.id]

    response = api_client.get(url, {"sort": "created_at", "order": "desc"})
    assert response.status_code == 200
    assert [r["room_id"] for r in response.data] == [newer.id, older.id]
