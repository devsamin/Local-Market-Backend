# from django.contrib import admin
# from .models import Order, OrderItem

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "total_price", "status", "created_at")
#     list_filter = ("status",)
#     search_fields = ("user__username",)
#     inlines = [OrderItemInline]

# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ("id", "order", "product", "quantity", "price")


from django.contrib import admin
from .models import Order, OrderItem

# Inline for OrderItems in Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "seller", "quantity", "price", "status")
    # সব editable রাখছি, যদি কিছু readonly রাখতে চান, readonly_fields=("price",)

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "id")
    inlines = [OrderItemInline]

# Standalone OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "seller", "quantity", "price", "status")
    list_filter = ("status", "seller")
    search_fields = ("product__name", "order__id")
