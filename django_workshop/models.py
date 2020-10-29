from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(MinValueValidator(1))
    projector = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def is_avaible_today(self):
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if self.reservations.filter(date=today).count() == 0:
            return True
        else:
            return False


class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    comment = models.TextField(default="")

    class Meta:
        unique_together = ('date', 'room',)

    def __str__(self):
        return f"{self.room.name}: {self.date}"
