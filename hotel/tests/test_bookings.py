import datetime as dt

import pytest
from django.urls import reverse

from hotel.models import Booking


@pytest.mark.django_db
def test_create_booking_ok(api_client, room):
    url = reverse("bookings-create")
    payload = {
        "room_id": room.id,
        "date_start": "2021-12-30",
        "date_end": "2022-01-02",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert "booking_id" in response.data
    assert Booking.objects.count() == 1


@pytest.mark.django_db
def test_create_booking_invalid_dates(api_client, room):
    url = reverse("bookings-create")

    response = api_client.post(
        url,
        {"room_id": room.id, "date_start": "2021-13-40", "date_end": "2022-01-02"},
        format="json",
    )
    assert response.status_code == 400

    response = api_client.post(
        url,
        {"room_id": room.id, "date_start": "2022-02-10", "date_end": "2022-02-01"},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_list_bookings_sorted(api_client, room):
    Booking.objects.create(
        room=room, date_start=dt.date(2022, 1, 10), date_end=dt.date(2022, 1, 12)
    )
    Booking.objects.create(
        room=room, date_start=dt.date(2021, 12, 1), date_end=dt.date(2021, 12, 3)
    )

    url = reverse("bookings-list")
    response = api_client.get(url, {"room_id": room.id})

    assert response.status_code == 200
    assert [b["date_start"] for b in response.data] == [
        "2021-12-01",
        "2022-01-10",
    ]


@pytest.mark.django_db
def test_delete_booking(api_client, booking):
    url = reverse("bookings-delete", kwargs={"booking_id": booking.id})
    response = api_client.delete(url)

    assert response.status_code == 200
    assert Booking.objects.count() == 0
