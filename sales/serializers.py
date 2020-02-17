from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Inventory, Order


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        exclude = ()


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Order
        exclude = ()
