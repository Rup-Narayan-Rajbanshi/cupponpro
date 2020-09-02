from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from commonapp.models.affiliate import AffiliateLink
from commonapp.models.category import Category, SubCategory
from commonapp.models.company import Company, CompanyUser, FavouriteCompany
from commonapp.models.coupon import Coupon, Voucher
from commonapp.models.document import Document
from commonapp.models.facility import Facility
from commonapp.models.image import Image
from commonapp.models.links import SocialLink
from commonapp.models.rating import Rating

class AdminCategoryapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')

class AdminCompanyapp(admin.ModelAdmin):
    list_display = ('id', 'name')
    fieldsets = (
            (_("Company Info"), {
                'fields':(
                    'name', 'logo', 'phone_number', 'category', 'sub_category', 'author', 'currency'
                    )
                }
            ),

            (_("Company Address"), {
                'fields':(
                    'country', 'state', 'city', 'address', 'zip_code'
                    )
                }
            ),

            (_("Partner Client"), {'fields':('is_partner',)}),

            (_("Permission"), {'fields':('status',)}),)

class AdminCouponapp(admin.ModelAdmin):
    list_display = ('id', 'description', 'company', 'token')
    fieldsets = (
            (_("Coupon Info"), {
                'fields':(
                    'company', 'description', 'expiry_date', 'discount', 'content_type', 'object_id'
                )
            }
        ),
    )

class AdminImageapp(admin.ModelAdmin):
    list_display = ('id', 'image', 'content_type')
    fieldsets = (
            (_("Image Info"), {
                'fields':(
                    'image', 'content_type', 'object_id',
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

admin.site.register(AffiliateLink)
admin.site.register(Category, AdminCategoryapp)
admin.site.register(Company, AdminCompanyapp)
admin.site.register(CompanyUser)
admin.site.register(Coupon, AdminCouponapp)
admin.site.register(Document)
admin.site.register(Facility)
admin.site.register(FavouriteCompany)
admin.site.register(Image, AdminImageapp)
admin.site.register(Rating, AdminRatingapp)
admin.site.register(SocialLink)
admin.site.register(SubCategory)
admin.site.register(Voucher)
