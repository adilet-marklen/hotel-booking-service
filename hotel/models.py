from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F


class Room(models.Model):
    description = models.TextField()
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f"Room #{self.pk}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(date_end__gte=F("date_start")),
                name="booking_date_end_gte_date_start",
            ),
        ]
        indexes = [
            models.Index(fields=["room", "date_start"]),
        ]

    def __str__(self) -> str:
        return f"Booking #{self.pk} for Room #{self.room_id}"
