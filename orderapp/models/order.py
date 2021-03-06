from django.contrib.postgres.fields import JSONField
from django.db import models, transaction
from django.db.models import Sum
from rest_framework.exceptions import APIException

from helpers.models import BaseModel
from company.models.asset import Asset
from company.models.company import Company
from company.models.partner import DeliveryPartner
from productapp.models.coupon import Voucher
from productapp.models.product import Product
from userapp.models.user import User
from helpers.constants import MAX_LENGTHS, DEFAULTS, ORDER_STATUS, DISCOUNT_TYPE, ORDER_LINE_STATUS
from helpers.choices_variable import ORDER_STATUS_CHOICES, ORDER_LINE_STATUS_CHOICES


class Orders(BaseModel):
    takeaway = models.ForeignKey(DeliveryPartner, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='orders')
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='orders', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='orders')
    status = models.CharField(max_length=MAX_LENGTHS['ORDER_STATUS'], choices=ORDER_STATUS_CHOICES, default=DEFAULTS['ORDER_STATUS'])
    extras = JSONField(blank=True, null=True)
    custom_discount_percentage = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    custom_discount_amount  = models.PositiveIntegerField(default = 0)
    is_service_charge = models.BooleanField(default=True)
    service_charge = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    payable_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)


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
        is_service_charge = v_data.get('is_service_charge', True)
        paid_amount = v_data.get('paid_amount', 0.0)
        payment_mode = v_data.pop('payment_mode', 'CASH')
        order.status = status
        order.custom_discount_percentage = custom_discount_percentage if 'custom_discount_percentage' in v_data else order.custom_discount_percentage
        order.custom_discount_amount = custom_discount_amount if 'custom_discount_amount' in v_data else order.custom_discount_amount
        order.is_service_charge = is_service_charge if 'is_service_charge' in v_data else order.is_service_charge

        order.save()
        payable_amount, tax = cls.get_grand_total(order)
        payable_amount = round(payable_amount, 6)
        order.payable_amount = payable_amount
        order.tax = tax
        service_charge_get = round(cls.service_charge_amount_static(order),2) if order.is_service_charge else 0
        order.service_charge = service_charge_get
        order.save()
        if status == ORDER_STATUS['BILLABLE']:
            data = dict()
            data['order'] = order.id
            data['company'] = order.company.id
            data['service_charge'] = service_charge_get
            data['payable_amount'] = payable_amount
            data['tax'] = tax
            data['paid_amount'] = paid_amount
            data['custom_discount_amount'] = order.custom_discount_amount
            data['custom_discount_percentage'] = order.custom_discount_percentage
            data['is_service_charge'] = order.is_service_charge
            data['payment_mode'] = payment_mode
            try:
                has_bill = order.bills is not None
            except:
                has_bill = False
            if has_bill:
                data['credit_amount'] = payable_amount
                serializer = BillCreateSerializer(instance=order.bills, data=data, context={'request': request}, partial=True)
                if not serializer.is_valid(raise_exception=True):
                    raise APIException(detail='Cannot update bill. ', code=400)
            else:
                serializer = BillCreateSerializer(data=data, context={'request': request})
                if not serializer.is_valid(raise_exception=True):
                    raise APIException(detail='Cannot bill the order', code=400)
            serializer.save()
            lines = order.lines.first()
            if lines.voucher:
                lines.voucher.is_redeem = True
                lines.voucher.save()

        if status == ORDER_STATUS['COMPLETED']:
            try:
                has_bill = order.bills is not None
            except:
                has_bill = False
            if has_bill:
                data = dict()
                data['order'] = order.id
                if 'payment_mode' in v_data:
                    data['payment_mode'] = payment_mode
                data['paid_amouont'] = paid_amount if 'paid_amount' in v_data else 0
                if not order.bills.paid_amount > 0.0:
                    data['paid_amount'] = order.bills.credit_amount
                    data['is_paid'] = True
                else:
                    #data['paid_amount'] = order.bill.paid_amount
                    data['is_paid'] = False if order.bills.credit_amount > 0.0 else True
                print(data)
                serializer = BillCreateSerializer(instance=order.bills, data=data, context={'request': request}, partial=True)
                if not serializer.is_valid():
                    raise serializer.ValidationError(detail='Cannot update bill. ', code=400)
                serializer.save()
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
        subtotal = self.lines.all().aggregate(order_total=Sum('total'))['order_total']
        if subtotal:
            return float(subtotal)
        else:
            return float(0)

    @property
    def discount_amount(self):
        value = 0.0
        for line in self.lines.all():
            value = value + line.get_discounted_amount()
        if self.custom_discount_percentage:
            total_for_discount = float(self.get_total) + float(self.service_charge_amount)
            custom_discount = float(float(self.custom_discount_percentage)/100) * float(total_for_discount)
            value = value + custom_discount
        if self.custom_discount_amount:
            value = value + self.custom_discount_amount
        return value


    @property
    def service_charge_amount(self):
        service_charge = self.company.service_charge if self.company.service_charge else 0
        total = self.get_total
        return float(service_charge / 100) * float(total) if self.is_service_charge else 0

    @staticmethod
    def service_charge_amount_static(order):
        service_charge = order.company.service_charge if order.company.service_charge else 0
        total = order.get_total
        return float(service_charge / 100) * float(total) if order.is_service_charge else 0

    @property
    def tax_amount(self):
        tax = self.company.tax if self.company.tax else 0
        return float(tax / 100) * float(float(self.get_total) + float(self.service_charge_amount))

    @property
    def get_total(self):
        value = 0.0
        for line in self.lines.all():
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
        total = float(order.lines.all().aggregate(order_total=Sum('total'))['order_total']) if order.lines.all().aggregate(order_total=Sum('total'))['order_total'] else 0
        # taxed_amount = float(taxed_amount) / 100 * float(total) #if is_service_charge else 0
        grand_total = grand_total + total
        service_charge_amount = float(service_charge_amount) / 100 * float(grand_total) if order.is_service_charge else 0
        grand_total = grand_total + service_charge_amount
        discount_amount = order.get_discount_amount(order, grand_total)
        grand_total = grand_total - discount_amount
        # service_charge_amount = float(service_charge_amount) / 100 * float(grand_total) if order.is_service_charge else 0
        # grand_total = grand_total + service_charge_amount
        taxed_amount = float(taxed_amount) / 100 * float(grand_total)
        taxed_amount = round(taxed_amount, 2)
        grand_total = round(grand_total + taxed_amount, 2)
        return (grand_total, taxed_amount)

    @staticmethod
    def get_grand_total_report(order):
        grand_total=0.0
        taxed_amount = order.company.tax if order.company.tax else 0
        service_charge_amount = order.company.service_charge if order.company.service_charge else 0
        total = float(order.lines.all().aggregate(order_total=Sum('total'))['order_total']) if order.lines.all().aggregate(order_total=Sum('total'))['order_total'] else 0
        # taxed_amount = float(taxed_amount) / 100 * float(total) #if is_service_charge else 0
        grand_total = grand_total + total
        service_charge_amount = float(service_charge_amount) / 100 * float(total) if order.is_service_charge else 0 #if is_service_charge else 0
        grand_total = grand_total + service_charge_amount
        discount_amount = order.get_discount_amount(order, grand_total)
        grand_total = grand_total - discount_amount
        # service_charge_amount = float(service_charge_amount) / 100 * float(grand_total) if order.is_service_charge else 0
        # grand_total = grand_total + service_charge_amount
        taxed_amount = float(taxed_amount) / 100 * float(grand_total)
        grand_total = round(grand_total + taxed_amount, 2)
        return grand_total

    def get_discount_amount(self, order,  grand_total):
        value = 0.0
        if order.custom_discount_percentage:
            custom_discount = float(float(order.custom_discount_percentage)/100) * float(grand_total)
            value = value + custom_discount
        if order.custom_discount_amount:
            value = value + order.custom_discount_amount
        return value


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
    customer_comment = models.CharField(max_length=250,null=True, blank=True)
    new = models.PositiveIntegerField(null=True, blank=True, default=0)
    cooking = models.PositiveIntegerField(null=True, blank=True, default=0)
    served = models.PositiveIntegerField(null=True, blank=True, default=0)
    cancelled = models.PositiveIntegerField(null=True, blank=True, default=0)

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
                return (discount / 100)* self.rate
            return discount
        return 0

    def get_discounted_amount(self):
        return self.get_discount() * (self.quantity-self.cancelled)

    def line_total_no_discount(self):
        return (self.rate * (self.quantity-self.cancelled))

    def get_line_total(self):
        return (self.rate * (self.quantity - self.cancelled)) - self.get_discounted_amount()

    def save(self, *args, **kwargs):
        self.rate = self.rate if self.rate else self.product.total_price
        self.discount = self.get_discount()
        self.discount_amount = self.get_discounted_amount()
        self.total = self.get_line_total()
        return super().save(*args, **kwargs)
