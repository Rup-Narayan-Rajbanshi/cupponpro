from django.contrib import admin
from .models.bills import Bills
from .models.order import Orders
# Register your models here.
admin.site.register(Bills)
admin.site.register(Orders)
