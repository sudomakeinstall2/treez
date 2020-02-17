from django.urls import path

from .views import InventoryListView, InventoryDetailView

urlpatterns = [
    path('inventories/', InventoryListView.as_view(), name="inventory-list"),
    path('inventories/<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
]
