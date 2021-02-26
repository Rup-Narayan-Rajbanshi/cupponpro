from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from company.models import Partner
from company.models.likes import Like
# Register your models here.
class AdminPartnerapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'logo')
    fieldsets = (
        (_("Partner Info"), {
            'fields':(
                'name', 'link', 'logo'
            )
        }
        ),
    )

admin.site.register(Partner, AdminPartnerapp)
admin.site.register(Like)
