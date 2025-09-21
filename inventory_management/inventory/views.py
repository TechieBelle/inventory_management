from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InventoryItem, Category, InventoryChangeLog
from .serializers import InventoryItemSerializer, CategorySerializer, InventoryChangeLogSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only admins can create/update/delete categories.
    Regular users can only read (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        print(request.user)
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff
    


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Categories are global:
    - Admins: full CRUD
    - Regular users: read-only
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class InventoryItemViewSet(viewsets.ModelViewSet):
    """
    Inventory items are owned by a user.
    - Regular users can only see/manage their own items.
    - Admins (is_staff) can see/manage all items.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InventoryItemSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category__name"]
    ordering_fields = ["name", "quantity", "price", "date_added"]
    filterset_fields = {
        "category": ["exact"],
        "price": ["gte", "lte"],
        "quantity": ["gte", "lte"],
        "date_added": ["gte", "lte"],
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # admins see all
            return InventoryItem.objects.all()
        return InventoryItem.objects.filter(user=user)

    # 🔹 Reusable logging helper
    def _log_change(self, item, field, change_type, old_value, new_value, quantity_diff=None):
        InventoryChangeLog.objects.create(
            item=item,
            user=self.request.user,
            field_changed=field,
            change_type=change_type,
            old_value=old_value,
            new_value=new_value,
            quantity_changed=quantity_diff,
        )

    # CREATE: Log restock/price initialization
    def perform_create(self, serializer):
        item = serializer.save(user=self.request.user)
        if item.quantity > 0:
            self._log_change(item, "quantity", "restock", 0, item.quantity, quantity_diff=item.quantity)
        if item.price > 0:
            self._log_change(item, "price", "increase", 0, item.price)

    # UPDATE: Log quantity and price changes
    def perform_update(self, serializer):
        instance = self.get_object()
        old_quantity = instance.quantity
        old_price = instance.price
        updated_item = serializer.save()

        if updated_item.quantity != old_quantity:
            diff = updated_item.quantity - old_quantity
            change_type = "restock" if diff > 0 else "sale"
            self._log_change(updated_item, "quantity", change_type, old_quantity, updated_item.quantity, diff)

        if updated_item.price != old_price:
            diff = updated_item.price - old_price
            change_type = "increase" if diff > 0 else "decrease"
            self._log_change(updated_item, "price", change_type, old_price, updated_item.price)

    # DELETE: Log removal of item before deleting
    def perform_destroy(self, instance):
        if instance.quantity > 0:
            self._log_change(instance, "quantity", "delete", instance.quantity, 0, quantity_diff=-instance.quantity)
        if instance.price > 0:
            self._log_change(instance, "price", "delete", instance.price, 0)
        instance.delete()

    # CUSTOM ACTIONS
    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        threshold = int(request.query_params.get("threshold", 5))
        qs = InventoryItem.objects.filter(quantity__lt=threshold)
        if not request.user.is_staff:
            qs = qs.filter(user=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        item = self.get_object()
        logs = item.changes.all().order_by("-timestamp")
        serializer = InventoryChangeLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def audit(self, request):
        logs = InventoryChangeLog.objects.all().order_by("-timestamp")
        if not request.user.is_staff:
            logs = logs.filter(item__user=request.user)
        serializer = InventoryChangeLogSerializer(logs, many=True)
        return Response(serializer.data)


class InventoryChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Change logs for inventory items.
    - Regular users only see logs for their own items.
    - Admins see all logs.
    """
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["item__name", "user__username", "field_changed", "change_type"]
    ordering_fields = ["timestamp", "item__name", "user__username"]
    filterset_fields = ["field_changed", "change_type"]

    def get_queryset(self):
        qs = InventoryChangeLog.objects.all().order_by("-timestamp")
        if not self.request.user.is_staff:
            qs = qs.filter(item__user=self.request.user)
        return qs
