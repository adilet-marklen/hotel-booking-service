import datetime as dt

import pytest
from rest_framework.test import APIClient

from hotel.models import Booking, Room


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def room():
    return Room.objects.create(description="Test room", price=1000)


@pytest.fixture()
def booking(room):
    return Booking.objects.create(
        room=room, date_start=dt.date(2021, 12, 30), date_end=dt.date(2022, 1, 2)
    )
