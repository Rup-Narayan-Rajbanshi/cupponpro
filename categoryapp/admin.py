from django.contrib import admin
from categoryapp.models.category import Category, ProductCategory

class AdminCategoryapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')

class AdminProductCategoryapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')

admin.site.register(Category, AdminCategoryapp)
admin.site.register(ProductCategory, AdminProductCategoryapp)
