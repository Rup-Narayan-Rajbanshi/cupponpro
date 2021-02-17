from django.contrib.postgres.fields import JSONField
from django.db import models, transaction
from django.db.models import Sum
from rest_framework.exceptions import APIException

from helpers.models import BaseModel
from commonapp.models.asset import Asset
from commonapp.models.company import Company
from commonapp.models.coupon import Voucher
from commonapp.models.product import Product
from orderapp.models.bills import Bills
from userapp.models.user import User
from helpers.constants import MAX_LENGTHS, DEFAULTS, ORDER_STATUS, DISCOUNT_TYPE, ORDER_LINE_STATUS
from helpers.choices_variable import ORDER_STATUS_CHOICES, ORDER_LINE_STATUS_CHOICES


class Orders(BaseModel):
    bill = models.ForeignKey(Bills, on_delete=models.SET_NULL, null=True, related_name='orders')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='orders')
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='orders', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='orders')
    status = models.CharField(max_length=MAX_LENGTHS['ORDER_STATUS'], choices=ORDER_STATUS_CHOICES, default=DEFAULTS['ORDER_STATUS'])
    extras = JSONField(blank=True, null=True)
    custom_discount_percentage = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True)
    custom_discount_amount  = models.PositiveIntegerField(default = 0)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

    def to_representation_id(self, request=None):
        return self.id

    ## need to revise the logic along with serializer with new model
    @classmethod
    @transaction.atomic
    def execute_change_status(cls, order, v_data, request):
        from orderapp.serializers.bill import BillCreateSerializer
        status = v_data.get('status')
        custom_discount_percentage = v_data.get('custom_discount_percentage', 0)
        custom_discount_amount = v_data.get('custom_discount_amount', 0)
        order.status = status
        order.custom_discount_percentage = custom_discount_percentage
        order.custom_discount_amount = custom_discount_amount
        order.save()
        if status == ORDER_STATUS['COMPLETED']:
            data = dict()
            data['company'] = order.company.id
            data['service_charge'] = order.company.service_charge if order.company.service_charge else 0
            data['tax'] = order.company.tax if order.company.tax else 0
            data['custom_discount_percentage'] = custom_discount_percentage
<<<<<<< HEAD
            data['grand_total'] = cls.get_grand_total(order)
=======
            data['custom_discount_amount'] = custom_discount_amount
>>>>>>> bugfixes/bill_servicecharge_discount
            serializer = BillCreateSerializer(data=data, context={'request': request})
            if not serializer.is_valid():
                raise APIException(detail='Cannot bill the order', code=400)
            order.bill = serializer.save()
            order.save()
        return order

    def to_representation(self, request=None):
        return {
            "id": self.id,
            "status": self.status,
        }

    def get_bills(self):
        bills = self.bill.to_representation()
        return bills

    @property
    def subtotal(self):
        subtotal = self.lines.exclude(status=ORDER_LINE_STATUS['CANCELLED']
                                      ).aggregate(order_total=Sum('total'))['order_total']
        if subtotal:
            return float(subtotal)
        else:
            return float(0)

    @property
    def discount_amount(self):
        value = 0.0
        for line in self.lines.exclude(status=ORDER_LINE_STATUS['CANCELLED']):
            value = value + line.get_discounted_amount()
        if self.custom_discount_percentage:
            custom_discount = float(self.custom_discount_percentage/100) * float(self.grand_total)
            value = value + custom_discount
        if self.custom_discount_amount:
            value = value + self.custom_discount_amount
        return value

    @property
    def service_charge_amount(self):
        service_charge = self.company.service_charge if self.company.service_charge else 0
        return float(service_charge / 100) * float(self.get_total)

    @property
    def tax_amount(self):
        tax = self.company.tax if self.company.tax else 0
        return float(tax / 100) * float(self.get_total)

    @property
    def get_total(self):
        value = 0.0
        for line in self.lines.exclude(status=ORDER_LINE_STATUS['CANCELLED']):
            value = value + line.get_line_total()
        return float(value)

    @property
    def grand_total(self):
        return self.get_total + self.tax_amount + self.service_charge_amount

    @staticmethod
    def get_grand_total(order):
        grand_total=0.0
        taxed_amount = order.company.tax if order.company.tax else 0
        service_charge_amount = order.company.service_charge if order.company.service_charge else 0
        total = float(order.lines.aggregate(order_total=Sum('total'))['order_total']) if order.lines.aggregate(order_total=Sum('total'))['order_total'] else 0
        taxed_amount = float(taxed_amount) / 100 * float(total)
        service_charge_amount = float(service_charge_amount) / 100 * float(total) #if is_service_charge else 0
        grand_total = grand_total + total + taxed_amount + service_charge_amount
        return grand_total


class OrderLines(BaseModel):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_lines')
    rate = models.PositiveIntegerField(blank=True)                  ## product.total_price
    quantity = models.PositiveIntegerField()
    voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT, null=True, blank=True, related_name='order_lines')
    discount = models.PositiveIntegerField(null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_LINE_STATUS_CHOICES, default=DEFAULTS['ORDER_LINE_STATUS'])
    new = models.PositiveIntegerField(null=True, blank=True, default=0)
    cooking = models.PositiveIntegerField(null=True, blank=True, default=0)
    served = models.PositiveIntegerField(null=True, blank=True, default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "{0} (order {1}".format(self.id, self.order.id)

    def to_representation_id(self, request=None):
        return self.id

    def get_discount(self):
        if self.voucher:
            discount = self.voucher.coupon.discount
            discount_type = self.voucher.coupon.discount_type
            if discount_type == DISCOUNT_TYPE['PERCENTAGE']:
                return (discount / 100) * self.rate
            return discount
        return 0

    def get_discounted_amount(self):
        return self.get_discount() * self.quantity

    def get_line_total(self):
        return (self.rate * self.quantity) - self.get_discounted_amount()

    def save(self, *args, **kwargs):
        self.discount = self.get_discount()
        self.discount_amount = self.get_discounted_amount()
        self.rate = self.rate if self.rate else self.product.total_price
        self.total = self.get_line_total()
        return super().save(*args, **kwargs)
