from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from company.models import Partner
from company.models.likes import Like
from company.models.follow import Follows
from company.models.advertisement import Advertisement
from company.models.company import Company, CompanyUser, FavouriteCompany
from company.models.document import Document
from company.models.facility import Facility
from company.models.links import SocialLink
from company.models.rating import Rating
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


class AdminCompanyapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'key', 'invoice_counter')
    fieldsets = (
            (_("Company Info"), {
                'fields':(
                    'name', 'logo', 'logo_icon', 'phone_number', 'email', 'category', 'sub_category', 'author', 'description', 'currency', 'is_verified', 'is_affiliate', 'url', 'discount', 'discount_code', 'count', 'deal_of_the_day'
                    )
                }
            ),

            (_("Company Address"), {
                'fields':(
                    'country', 'state', 'city', 'address', 'longitude', 'latitude', 'zip_code'
                    )
                }
            ),
            (_("Billing"), {'fields':('service_charge', 'tax')}),
            (_("Partner Client"), {'fields':('is_partner',)}),

            (_("Permission"), {'fields':('status',)}),)


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


admin.site.register(Partner, AdminPartnerapp)
admin.site.register(Like)
admin.site.register(Follows)
admin.site.register(Advertisement)
admin.site.register(Company, AdminCompanyapp)
admin.site.register(CompanyUser)
admin.site.register(FavouriteCompany)
admin.site.register(SocialLink)
admin.site.register(Document)
admin.site.register(Facility)
admin.site.register(Rating, AdminRatingapp)
