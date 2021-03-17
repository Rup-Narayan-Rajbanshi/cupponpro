from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from commonapp.models.affiliate import AffiliateLink
from company.models.asset import Asset
from commonapp.models.bill import Bill
from commonapp.models.category import Category, SubCategory
from productapp.models.coupon import Coupon, Voucher
from commonapp.models.image import Image
from commonapp.models.order import Order, OrderLine
from productapp.models.product import BulkQuantity, Product, ProductCategory
from commonapp.models.salesitem import SalesItem


class AdminBillapp(admin.ModelAdmin):
    list_display = ('id', 'payment_mode', 'invoice_number', 'created_at')
    fieldsets = (
        (_("Basic info"), {
            'fields':('company', 'user', 'name', 'phone_number', 'payment_mode')
        }
        ),
    )

class AdminSalesItemapp(admin.ModelAdmin):
    list_display = ('id', 'rate', 'quantity',\
        'created_at')
    fieldsets = (
        (_("Basic info"), {
            'fields':(
                'bill', 'product', 'voucher', 'discount', 'quantity', 'rate', 'total'
            )
        }
        ),
    )

class AdminCategoryapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')



class CouponAdminForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'

    def clean_name(self):
        from helpers.validators import is_alphanumeric_with_exception
        name = self.cleaned_data['name']
        try:
            name = is_alphanumeric_with_exception(name)
        except Exception as e:
            raise forms.ValidationError(str(e.detail[0]))
        return name

    def clean_discount(self):
        from helpers.constants import DISCOUNT_TYPE
        from helpers.validators import is_positive_float
        discount = self.cleaned_data['discount']
        if self.cleaned_data['discount_type'] == DISCOUNT_TYPE['PERCENTAGE']:
            if discount > 100:
                raise forms.ValidationError('Discount cannot be greater then 100 for percentage discount type.')
        try:
            discount = is_positive_float(discount)
        except Exception as e:
            raise forms.ValidationError(str(e.detail[0]))
        return discount


class AdminCouponapp(admin.ModelAdmin):
    list_display = ('id', 'description', 'company', 'token')
    form = CouponAdminForm
    fieldsets = (
            (_("Coupon Info"), {
                'fields':(
                    'name', 'company', 'description', 'expiry_date', 'discount_type', 'discount', 'content_type', 'object_id', 'deal_of_the_day'
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

class AdminBulkQuantityapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')

class AdminProductapp(admin.ModelAdmin):
    list_display = ('id', 'product_code', 'name', 'total_price', 'created_at')

class AdminProductCategoryapp(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')



class Assetapp(admin.ModelAdmin):
    change_list_template = "custom_asset_page.html"

admin.site.register(AffiliateLink)
admin.site.register(Asset, Assetapp)
admin.site.register(Bill, AdminBillapp)
admin.site.register(BulkQuantity, AdminBulkQuantityapp)
admin.site.register(Category, AdminCategoryapp)
admin.site.register(Coupon, AdminCouponapp)
admin.site.register(Image, AdminImageapp)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Product, AdminProductapp)
admin.site.register(ProductCategory, AdminProductCategoryapp)
admin.site.register(SalesItem, AdminSalesItemapp)
admin.site.register(SubCategory)
admin.site.register(Voucher)
