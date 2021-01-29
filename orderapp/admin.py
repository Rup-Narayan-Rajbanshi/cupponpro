from django.contrib import admin
from .models.bills import Bills
from .models.order import Orders, OrderLines
# Register your models here.
admin.site.register(Bills)
admin.site.register(Orders)
admin.site.register(OrderLines)
