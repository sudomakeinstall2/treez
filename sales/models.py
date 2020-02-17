from collections import Counter

from django.contrib.auth.models import User
from django.db import models, transaction
from rest_framework.exceptions import ValidationError


class Inventory(models.Model):
    name = models.CharField(blank=False, max_length=50, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    @staticmethod
    def remove_from_inventory(inventories):
        Inventory.__adjust_inventories(inventories, decrease=True)

    @staticmethod
    def add_to_inventory(inventories):
        Inventory.__adjust_inventories(inventories, decrease=False)

    @staticmethod
    def __adjust_inventories(inventories, decrease=False):
        counter = Counter(inventories)
        with transaction.atomic():
            for pk in counter:
                inventory = Inventory.objects.get(pk=pk)
                if decrease:
                    new_val = inventory.quantity - counter[pk]
                else:
                    new_val = inventory.quantity + counter[pk]
                inventory.quantity = new_val
                if inventory.quantity < 0:
                    raise ValidationError(
                        "Can not order more than inventory availability."
                    )
                inventory.save()


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
