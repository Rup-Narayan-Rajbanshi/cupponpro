from django.contrib import admin

# Register your models here.
from commonapp.models import Address, Company


from django.utils.translation import ugettext_lazy as _


class AdminCompanyapp(admin.ModelAdmin):
    list_display = ('id', 'name')
    fieldsets = (
            (_("Company info"), {
                'fields':(
                    'name', 'image', 'phone', 'category', 'author'
                    )
                }
            ),

            (_("Company Address"), {
                'fields':(
                    'country', 'state', 'city', 'address1', 'address2'
                    )
                }
            ),

            (_("Permission"), {'fields':('status',)}),)


admin.site.register(Company, AdminCompanyapp)
