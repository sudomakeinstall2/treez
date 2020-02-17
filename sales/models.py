from django.contrib.auth.models import User
from django.db import models


class Inventory(models.Model):
    name = models.CharField(blank=False, max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    CREATED = "created"
    CANCELLED = "cancelled"
    FINISHED = "finished"

    STATUS_CHOICES = (
        (CREATED, "created"),
        (CANCELLED, "cancelled"),
        (FINISHED, "finished"),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    inventories = models.ManyToManyField(Inventory)

