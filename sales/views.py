from rest_framework import generics

from .serializers import InventorySerializer
from .models import Inventory


class InventoryListView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

