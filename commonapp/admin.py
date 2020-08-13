from django.contrib import admin

# Register your models here.
from commonapp.models.company import Address, Company, Coupon
from commonapp.models.rating import Rating

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

class AdminCouponapp(admin.ModelAdmin):
    list_display = ('id', 'company', 'token')
    fieldsets = (
            (_("Company info"), {
                'fields':(
                    'company', 'token_expiry_date', 'discount', 'product_name', 'price', 'image'
                )
            }
        ),
    )

class AdminRatingapp(admin.ModelAdmin):
    list_display = ('id', 'company', 'description', 'user', 'rate')
    fieldsets = (
        (_("Rating Info"), {
            'fields':(
                'company', 'description', 'user', 'rate'
            )
        }
        ),
    )

admin.site.register(Company, AdminCompanyapp)
admin.site.register(Coupon, AdminCouponapp)
admin.site.register(Rating, AdminRatingapp)