from django.contrib import admin

# Register your models here.
from billapp.models.bill import Bill
from billapp.models.salesitem import Salesitem

from django.utils.translation import ugettext_lazy as _

class AdminBillapp(admin.ModelAdmin):
    list_display = ('id', 'company', 'user', 'total', 'discount_percentage',\
        'discount', 'grand_total', 'created_at')
    fieldsets = (
        (_("Basic info"), {
            'fields':(
                'company', 'user', 'total', 'discount_percentage',\
                'discount', 'grand_total'
            )
        }
        ),
    )

class AdminSalesitemapp(admin.ModelAdmin):
    list_display = ('id', 'bill', 'product', 'amount', 'quantity',\
        'created_at')
    fieldsets = (
        (_("Basic info"), {
            'fields':(
                'bill', 'product', 'amount', 'quantity'
            )
        }
        ),
    )

admin.site.register(Bill, AdminBillapp)
admin.site.register(Salesitem, AdminSalesitemapp)