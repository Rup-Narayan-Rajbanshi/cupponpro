from django.contrib import admin
from productapp.models.product import BulkQuantity, Product, ProductCategory

class AdminBulkQuantityapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')

class AdminProductapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'total_price', 'created_at')

class AdminProductCategoryapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')

admin.site.register(BulkQuantity, AdminBulkQuantityapp)
admin.site.register(Product, AdminProductapp)
admin.site.register(ProductCategory, AdminProductCategoryapp)
