from django.contrib import admin

# Register your models here.
from bannerapp.models.banner import Banner


from django.utils.translation import ugettext_lazy as _


class AdminBannerapp(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'active', 'created_at')
    fieldsets = (
            (_("Basic info"), {
                'fields':(
                    'title', 'description', 'image', 'url'
                    )
                }
            ),
            (_("Active"), {'fields':('active',)}),)


admin.site.register(Banner, AdminBannerapp)
