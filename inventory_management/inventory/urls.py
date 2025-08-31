# inventory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, CategoryViewSet, InventoryChangeLogViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"items", InventoryItemViewSet, basename="item")
router.register(r"changes", InventoryChangeLogViewSet, basename="change")

urlpatterns = [
    path("", include(router.urls)),
]
