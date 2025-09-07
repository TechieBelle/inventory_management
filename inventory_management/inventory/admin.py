from django.contrib import admin
from .models import Category,InventoryItem, InventoryChangeLog
# Register your models here.

admin.site.register(Category)
admin.site.register(InventoryItem)
admin.site.register(InventoryChangeLog)