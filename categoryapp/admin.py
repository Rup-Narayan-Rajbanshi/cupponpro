from django.contrib import admin

# Register your models here.
from categoryapp.models import Category


from django.utils.translation import ugettext_lazy as _


class AdminCategoryapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')


admin.site.register(Category, AdminCategoryapp)
