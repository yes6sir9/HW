from django.db import models

class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'Table {self.number} ({self.seats} seats)'
