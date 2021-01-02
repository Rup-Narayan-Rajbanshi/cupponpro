from django.db import models, transaction
from rest_framework.exceptions import APIException

from helpers.models import BaseModel
from commonapp.models.asset import Asset
from commonapp.models.company import Company
from commonapp.models.coupon import Voucher
from commonapp.models.product import Product
from orderapp.models.bills import Bills
from userapp.models.user import User
from helpers.constants import MAX_LENGTHS, DEFAULTS, ORDER_STATUS, DISCOUNT_TYPE
from helpers.choices_variable import ORDER_STATUS_CHOICES, ORDER_LINE_STATUS_CHOICES


class Orders(BaseModel):
    bill = models.ForeignKey(Bills, on_delete=models.SET_NULL, null=True, related_name='orders')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='orders')
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='orders')
    status = models.CharField(max_length=MAX_LENGTHS['ORDER_STATUS'], choices=ORDER_STATUS_CHOICES, default=DEFAULTS['ORDER_STATUS'])

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

    ## need to revise the logic along with serializer with new model
    @classmethod
    @transaction.atomic
    def execute_change_status(cls, order, v_data, request):
        from orderapp.serializers.bill import BillCreateSerializer
        status = v_data.get('status')
        order.status = status
        order.save()
        if status == ORDER_STATUS['BILLABLE']:
            data = dict()
            data['company'] = order.company.id
            data['service_charge'] = order.company.service_charge if order.company.service_charge else 0
            data['tax'] = order.company.tax if order.company.tax else 0
            serializer = BillCreateSerializer(data=data, context={'request': request})
            if not serializer.is_valid():
                raise APIException(detail='Cannot bill the order', code=400)
            order.bill = serializer.save()
            order.save()
        return order

    def to_representation(self, request=None):
        return {
            "id": self.id,
            "status": self.status
        }

    def get_bills(self):
        bills = self.bill.to_representation()
        return bills


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
        self.total = self.get_line_total()
        return super().save(*args, **kwargs)
