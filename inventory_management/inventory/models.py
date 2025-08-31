from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"


class InventoryChangeLog(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="changes")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field_changed = models.CharField(
        max_length=50,
        choices=[("quantity", "Quantity"), ("price", "Price")]
    )
    change_type = models.CharField(
        max_length=20,
        choices=[("restock", "Restock"), ("sale", "Sale"), ("increase", "Increase"), ("decrease", "Decrease")]
    )
    old_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    new_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    quantity_changed = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.field_changed} {self.change_type}"
