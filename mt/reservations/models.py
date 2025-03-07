from django.db import models
from customers.models import Customer
from tables.models import Table

STATUS_CHOICES = [
    ("ожидает", "Ожидает"),
    ("подтверждено", "Подтверждено"),
    ("отменено", "Отменено"),
]

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ожидает")

    def __str__(self):
        return f'Reservation {self.id} - {self.customer.name} ({self.status})'
