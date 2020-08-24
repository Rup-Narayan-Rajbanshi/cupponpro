from django.contrib import admin

# Register your models here.
from bannerapp.models import Banner


from django.utils.translation import ugettext_lazy as _


class AdminBannerapp(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'status', 'created_at')
    fieldsets = (
            (_("Basic info"), {
                'fields':(
                    'title', 'description', 'image'
                    )
                }
            ),
            (_("Permission"), {'fields':('status',)}),)


admin.site.register(Banner, AdminBannerapp)
