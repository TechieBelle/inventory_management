from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InventoryItem, Category, InventoryChangeLog
from .serializers import InventoryItemSerializer, CategorySerializer, InventoryChangeLogSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InventoryItem, Category, InventoryChangeLog
from .serializers import InventoryItemSerializer, CategorySerializer, InventoryChangeLogSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category__name"]
    ordering_fields = ["name", "quantity", "price", "date_added"]
    filterset_fields = {
        "category": ["exact"],          # filter by category id
        "price": ["gte", "lte"],        # price range: greater than equal, less than equal
        "quantity": ["gte", "lte"],     # low stock / high stock thresholds
        "date_added": ["gte", "lte"],   # items added in a date range
    }

    def get_queryset(self):
        return InventoryItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        item = serializer.save(user=self.request.user)
        if item.quantity > 0:
            InventoryChangeLog.objects.create(
                item=item,
                user=self.request.user,
                field_changed="quantity",
                change_type="restock",
                old_value=0,
                new_value=item.quantity,
                quantity_changed=item.quantity,
            )
        if item.price > 0:
            InventoryChangeLog.objects.create(
                item=item,
                user=self.request.user,
                field_changed="price",
                change_type="increase",
                old_value=0,
                new_value=item.price,
            )

    def perform_update(self, serializer):
        instance = self.get_object()
        old_quantity = instance.quantity
        old_price = instance.price
        updated_item = serializer.save()

        if updated_item.quantity != old_quantity:
            diff = updated_item.quantity - old_quantity
            change_type = "restock" if diff > 0 else "sale"
            InventoryChangeLog.objects.create(
                item=updated_item,
                user=self.request.user,
                field_changed="quantity",
                change_type=change_type,
                old_value=old_quantity,
                new_value=updated_item.quantity,
                quantity_changed=diff,
            )

        if updated_item.price != old_price:
            diff = updated_item.price - old_price
            change_type = "increase" if diff > 0 else "decrease"
            InventoryChangeLog.objects.create(
                item=updated_item,
                user=self.request.user,
                field_changed="price",
                change_type=change_type,
                old_value=old_price,
                new_value=updated_item.price,
            )

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        threshold = int(request.query_params.get("threshold", 5))
        qs = InventoryItem.objects.filter(quantity__lt=threshold, user=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        item = self.get_object()
        logs = item.changes.all().order_by("-timestamp")
        serializer = InventoryChangeLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def audit(self, request, pk=None):
        item = self.get_object()
        logs = item.changes.all().order_by("-timestamp")
        serializer = InventoryChangeLogSerializer(logs, many=True)
        return Response(serializer.data)



class InventoryChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["item__name", "user__username", "field_changed", "change_type"]
    ordering_fields = ["timestamp", "item__name", "user__username"]
    filterset_fields = ["field_changed", "change_type"]

    def get_queryset(self):
        return (
            InventoryChangeLog.objects
            .filter(item__user=self.request.user)
            .order_by("-timestamp")
        )