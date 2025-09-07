from rest_framework import serializers
from .models import InventoryItem, Category, InventoryChangeLog


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class InventoryItemSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)


    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "name",
            "description",
            "quantity",
            "price",
            "user_name",      # ✅ added
            "category",
            "category_name",  # ✅ added
             "date_added",
            "last_updated",
        ]
        read_only_fields = ("user", "date_added", "last_updated")

# class InventoryItemSerializer(serializers.ModelSerializer):
#     user_name = serializers.CharField(source="user.username", read_only=True)
#     class Meta:
#         model = InventoryItem
#         fields = "__all__"
#         read_only_fields = ("user", "date_added", "last_updated")


class InventoryChangeLogSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = InventoryChangeLog
        fields = "__all__"
