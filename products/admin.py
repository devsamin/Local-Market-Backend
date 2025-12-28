from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_categories', 'price', 'stock' ,'discount', 'is_available']
    # list_filter = ['is_available']
    search_fields = ['name']

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = "Categories"
