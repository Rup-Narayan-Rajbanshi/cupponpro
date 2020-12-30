from rest_framework.exceptions import APIException
from django.db import models, transaction
from helpers.models import BaseModel
from commonapp.models.asset import Asset
from commonapp.models.bill import Bill
from commonapp.models.company import Company
from commonapp.models.coupon import Voucher
from commonapp.models.product import Product
from userapp.models.user import User
from helpers.constants import MAX_LENGTHS, DEFAULTS, ORDER_STATUS, DISCOUNT_TYPE
from helpers.choices_variable import ORDER_STATUS_CHOICES, ORDER_LINE_STATUS_CHOICES
from commonapp.app_helper import Request


class Orders(BaseModel):
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, related_name='orders')
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
        from commonapp.api.salesitem import SalesItemVerifyView
        from commonapp.serializers.bill import BillSaveSerializer
        status = v_data.get('status')
        order.status = status
        order.save()
        if status == ORDER_STATUS['BILLABLE']:
            request_user = request.user if request else None
            verify_class = SalesItemVerifyView()
            order_dict = order.__dict__
            pop_items = ['is_billed', 'created_at', 'status']
            for pop_item in pop_items:
                order_dict.pop(pop_item, None)
            rename_keys = {
                'bill_id': 'bill',
                'company_id': 'company',
                'asset_id': 'asset',
                'user_id': 'user',
                'voucher_id': 'voucher'
            }
            for key, renamed in rename_keys.items():
                order_dict[renamed] = order_dict[key] if hasattr(order_dict, key) else None
                order_dict.pop(key, None)
            order_lines = OrderLines.objects.filter(order=order).values()
            order_dict['sales_item'] = list()
            for order_line in order_lines:
                line = dict()
                line['id'] = None
                line['order'] = str(order_line.get('id'))
                line['company'] = order_line.get('company_id')
                line['product'] = order_line.get('product_id')
                line['rate'] = order_line.get('rate')
                line['quantity'] = order_line.get('quantity')
                line['total'] = order_line.get('total')
                order_dict['sales_item'].append(line)
            custom_request = Request()
            custom_request.set_data(order_dict)
            verified_data = verify_class.sales_calculation(custom_request, order.company.id)
            serializer = BillSaveSerializer(data=verified_data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
            else:
                raise APIException(detail=serializer.errors, code=400)
            data = serializer.data
            order.is_billed = True
            order.bill = Bill.objects.filter(id=data.get('id')).first()
            order.save()
        return order

    def to_representation(self, request=None):
        return {
            "id": self.id,
            "status": self.status
        }

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
