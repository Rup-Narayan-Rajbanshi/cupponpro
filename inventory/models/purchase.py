from django.db import models
from commonapp.models.company import Company
from helpers.models import BaseModel
from inventory.models.stock import Stock
from helpers.constants import DEFAULTS
from helpers.choices_variable import PURCHASE_STATUS_CHOICES, PAYMENT_CHOICES, STOCK_TRANSACTION_CHOICES
from django.utils import timezone
from inventory.models.supplier import Supplier
from django.db import transaction
from rest_framework.exceptions import ValidationError



class Purchase(BaseModel):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=False, default=0)
    unit = models.CharField(max_length=10, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(default=None, blank=True)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, default=0)
    status = models.CharField(max_length=16, choices=PURCHASE_STATUS_CHOICES, default=DEFAULTS['PURCHASE_STATUS'])
    document = models.FileField(upload_to="document/", blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=False, default=0)
    total_amount = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=False, default=0)
    credit_amount = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=False, default=0)
    is_credit = models.BooleanField(default=True)
    discount_percent = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=False, default=0)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default=DEFAULTS['PAYMENT_CHOICES'])
    types = models.CharField(max_length=15, choices=STOCK_TRANSACTION_CHOICES, default=DEFAULTS['STOCK_TRANSACTION'])


    def to_representation(self, request=None):
        return {
            'id': self.id,
            'name': self.stock.name
        }


    @classmethod
    @transaction.atomic
    def create_purchase(cls, **kwargs):
        payment_note = kwargs.pop('payment_note', '')
        paid_date = kwargs.pop('paid_date', None)
        unit_cost = kwargs.get('unit_cost', 0.0)
        quantity = kwargs.get('quantity', 0.0)
        discount_percent = kwargs.get('discount_percent', 0.0)
        paid_amount = float(kwargs.get('paid_amount', 0.0))
        kwargs['total_amount'] = cls.get_total_amount(unit_cost, quantity, discount_percent)
        kwargs['credit_amount'] = cls.get_credit_amount(kwargs['total_amount'], paid_amount)
        kwargs['is_credit'] = cls.get_is_credit(kwargs['credit_amount'])
        if paid_amount > kwargs['total_amount']:
            raise ValidationError({'detail':'Paid amount exceeded total amount'})
        purchase = cls.objects.create(**kwargs)
        stock = None
        if purchase.status == 'RECEIVED' and purchase.types == 'PURCHASE':
            stock = Stock.objects.filter(id=purchase.stock.id).first()
            if stock:
                stock_amount = stock.stock
                stock.update(stock=float(stock_amount) + float(purchase.quantity), unit=purchase.unit)
        elif purchase.types == 'DISPATCH':
            stock = Stock.objects.filter(id=purchase.stock.id).first()
            if stock:
                stock_amount = stock.stock
                stock.update(stock=float(stock_amount) - float(purchase.quantity))
        elif purchase.types == 'RETURN' and purchase.status == 'RECEIVED':
            stock = Stock.objects.filter(id=purchase.stock.id).first()
            if stock:
                stock_amount = stock.stock
                stock.update(stock=float(stock_amount) - float(purchase.quantity))
        if paid_amount > 0.0:
            data = {'paid_amount': paid_amount, 'purchase': purchase.id, 'payment_note': payment_note, 'paid_date': paid_date, 
                    'payment_mode':kwargs.get('payment_mode', 'CASH'), 'credit_amount': kwargs.get('credit_amount')}
            PurchaseTransaction.create_transaction(**data)
        return (purchase, stock)

    @classmethod
    @transaction.atomic
    def update_purchase(cls, instance, **kwargs):
        paid_amount = float(kwargs.get('paid_amount', 0.0))
        kwargs['paid_amount'] = paid_amount + + float(instance.paid_amount)
        payment_note = kwargs.pop('payment_note', '') 
        paid_date = kwargs.pop('paid_date', None)
        unit_cost = kwargs.get('unit_cost') if 'unit_cost' in kwargs else instance.unit_cost
        quantity = kwargs.get('quantity') if 'quantity' in kwargs else instance.quantity
        discount_percent = kwargs.get('discount_percent') if 'discount_percent' in kwargs else instance.discount_percent
        kwargs['total_amount'] = cls.get_total_amount(unit_cost, quantity, discount_percent)
        kwargs['credit_amount'] = cls.get_credit_amount(kwargs['total_amount'], kwargs['paid_amount'])
        kwargs['is_credit'] = cls.get_is_credit(kwargs['credit_amount'])
        if kwargs['paid_amount'] > kwargs['total_amount']:
            raise ValidationError({'detail':'Paid amount exceeded total amount'})
        purchase = instance.update(**kwargs)
        if paid_amount > 0.0:
            data = {'paid_amount': paid_amount, 'purchase': purchase, 'payment_note': payment_note, 'paid_date': paid_date, 
                    'payment_mode':kwargs.get('payment_mode', 'CASH'), 'credit_amount': kwargs.get('credit_amount')}
            PurchaseTransaction.create_transaction(**data)
        return purchase





    @staticmethod
    def get_total_amount(unit_cost, purchase_quantity, discount_percent):
        total = float(unit_cost) * float(purchase_quantity)
        discount = float(total) * float(discount_percent)/100
        total_with_discout = total - discount
        return total_with_discout

    @staticmethod
    def get_credit_amount(total_amount, paid_amount):
        return float(total_amount) - float(paid_amount)
    
    @staticmethod
    def get_is_credit(credit_amount):
        if not credit_amount > 0.0:
            return False
        else:
            return True






class PurchaseTransaction(BaseModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=False, default=0)
    paid_date = models.DateField(default=None, blank=True)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default=DEFAULTS['PAYMENT_CHOICES'])
    credit_amount = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=False, default=0)
    payment_note = models.CharField(max_length=128, blank=True, null=True)

    @classmethod
    @transaction.atomic
    def create_transaction(cls, **kwargs):
        transaction = cls.objects.create(**kwargs)
        return transaction
