from django.contrib import admin
from productapp.models.product import BulkQuantity, Product

class AdminBulkQuantityapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')

class AdminProductapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'total_price', 'created_at')

admin.site.register(BulkQuantity, AdminBulkQuantityapp)
admin.site.register(Product, AdminProductapp)
