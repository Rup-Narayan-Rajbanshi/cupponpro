from django.contrib import admin

# Register your models here.
from billapp.models.bill import Bill
from billapp.models.salesitem import Salesitem

from django.utils.translation import ugettext_lazy as _

class AdminBillapp(admin.ModelAdmin):
    list_display = ('id', 'total', 'total_discount', 'tax', 'taxed_amount',\
        'grand_total', 'payment_mode', 'created_at')
    fieldsets = (
        (_("Basic info"), {
            'fields':(
                'company', 'user', 'name', 'phone_number', 'total', 'total_discount', 'tax', \
                'taxed_amount', 'grand_total', 'payment_mode'
            )
        }
        ),
    )

class AdminSalesitemapp(admin.ModelAdmin):
    list_display = ('id', 'amount', 'quantity', 'currency', \
        'created_at')
    fieldsets = (
        (_("Basic info"), {
            'fields':(
                'bill', 'product', 'amount', 'quantity', 'currency'
            )
        }
        ),
    )

admin.site.register(Bill, AdminBillapp)
admin.site.register(Salesitem, AdminSalesitemapp)