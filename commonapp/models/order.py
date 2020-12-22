import uuid
from django.core.validators import RegexValidator
from rest_framework.exceptions import APIException
from django.db import models, transaction
from django.db.models import F
from commonapp.models.asset import Asset
from commonapp.models.bill import Bill
from commonapp.models.company import Company
from commonapp.models.coupon import Voucher
from commonapp.models.product import Product
from userapp.models.user import User
from helpers.constants import MAX_LENGTHS, DEFAULTS, ORDER_STATUS
from helpers.choices_variable import ORDER_STATUS_CHOICES, ORDER_LINE_STATUS, ORDER_LINE_STATUS_CHOICES
from commonapp.app_helper import Request


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=False, blank=True,\
        validators=[RegexValidator(regex=r"^(\+?[\d]{2,3}\-?)?[\d]{8,10}$")])
    email = models.EmailField(max_length=50, null=False, blank=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True)
    is_billed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=MAX_LENGTHS['ORDER_STATUS'], choices=ORDER_STATUS_CHOICES, default=DEFAULTS['ORDER_STATUS'])

    class Meta:
        db_table = 'order'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        ''' Registered User's information saved, or saved from UI input '''
        if self.user:
            self.name = self.user.full_name
            self.email = self.user.email
            self.phone_number = self.user.phone_number
        return super(Order, self).save(*args, **kwargs)

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
                order_dict.pop(pop_item)
            rename_keys = {
                'bill_id': 'bill',
                'company_id': 'company',
                'asset_id': 'asset',
                'user_id': 'user',
                'voucher_id': 'voucher'
            }
            for key, renamed in rename_keys.items():
                order_dict[renamed] = order_dict[key]
                order_dict.pop(key, None)
            order_lines = OrderLine.objects.filter(order=order).values()
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


class OrderLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    rate = models.PositiveIntegerField(blank=True)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=20, choices=ORDER_LINE_STATUS_CHOICES, default=DEFAULTS['ORDER_LINE_STATUS'])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_line'
        ordering = ['-created_at']

    def __str__(self):
        return "order " + str(self.id) + " of " + str(self.company.name)

    def to_representation_id(self, request=None):
        return self.id

    def save(self, *args, **kwargs):
        ''' On save, create key '''
        if not self.rate:
            self.rate = self.product.total_price
        return super(OrderLine, self).save(*args, **kwargs)
