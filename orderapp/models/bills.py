from django.db import models
from django.db.models import Sum

from commonapp.models.company import Company
from helpers.models import BaseModel
from orderapp.choice_variables import PAYMENT_CHOICES
# from orderapp.constants import PAYMENT_MODES
from orderapp.constants import DEFAULTS


class Bills(BaseModel):
    ## these options needs to be moved in helpers/constant and choices variable and letter should be UPPER CASE
    # Payment Modes
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    customer = models.ForeignKey('userapp.Customer', on_delete=models.SET_NULL, null=True, related_name='bills')
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default=DEFAULTS['PAYMENT_CHOICES'])
    service_charge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_service_charge = models.BooleanField(default=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    payable_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    is_credit = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=8, editable=False)
    is_manual = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    custom_discount_percentage = models.PositiveIntegerField(default=0)
    credit_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    ret_amount  = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    
    custom_discount_amount  = models.PositiveIntegerField(default = 0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

    # need to revise as well, reve this as possible
    def save(self, *args, **kwargs):
        ''' Registered User's information saved, or saved from UI input '''
        
        if not self.invoice_number:
            company_obj = Company.objects.get(id=self.company_id)
            company_obj.invoice_counter += 1
            company_obj.save()
            invoice_number = str(company_obj.invoice_counter)
            self.invoice_number = "0" * (8 - len(invoice_number)) + invoice_number
        if self._state.adding == False:
            if float(self.credit_amount) - float(self.paid_amount) < 0.0:
                self.ret_amount = float(self.paid_amount) - float(self.credit_amount)
                self.paid_amount = self.credit_amount
            else:
                self.ret_amount = 0.0
            self.is_credit = self.is_credited(self.credit_amount, self.paid_amount)
            self.credit_amount = self.credited_amount(self.credit_amount, self.paid_amount)
        else:
            if float(self.payable_amount) - float(self.paid_amount) < 0.0:
                self.ret_amount = float(self.paid_amount) - float(self.payable_amount)
                self.paid_amount = self.payable_amount
            else:
                self.ret_amount=0.0
            self.is_credit = self.is_credited(self.payable_amount, self.paid_amount)
            self.credit_amount = self.credited_amount(self.payable_amount, self.paid_amount)
        return super(Bills, self).save(*args, **kwargs)
        

    def get_grand_total(self):
        # if self.payable_amount:
        #     grand_total=float(self.payable_amount)
        # else:
        grand_total = 0.0

        for order in self.orders.all():
            taxed_amount = self.company.tax if self.company.tax else 0
            service_charge_amount = self.company.service_charge if self.company.service_charge else 0
            total = float(order.lines.exclude(status=ORDER_LINE_STATUS['CANCELLED'].aggregate(order_total=Sum('total'))['order_total']) if order.lines.aggregate(order_total=Sum('total'))['order_total'] else 0
            # taxed_amount = float(taxed_amount) / 100 * float(total)
            grand_total = grand_total + total 
            discount_amount = self.get_discount_amount(grand_total)
            grand_total = grand_total - discount_amount 
            service_charge_amount = float(service_charge_amount) / 100 * float(grand_total) if order.is_service_charge else 0
            grand_total = grand_total + service_charge_amount
            taxed_amount = float(taxed_amount) / 100 * float(grand_total)
            grand_total = grand_total + taxed_amount
        return grand_total

    def get_discount_amount(self, grand_total):
        value = 0.0
        if self.custom_discount_percentage:
            custom_discount = float(self.custom_discount_percentage/100) * float(grand_total)
            value = value + custom_discount
        if self.custom_discount_amount:
            value = value + self.custom_discount_amount
        return value
        

    def get_subtotal(self):
        subtotal = 0
        discount_amount = 0
        try:
            voucher = self.orders.first().lines.first().voucher
        except:
            voucher = None
        for order in self.orders.all():
            try:
                total = float(order.lines.exclude(status=ORDER_LINE_STATUS['CANCELLED'].aggregate(order_total=Sum('total'))['order_total'])
                subtotal = subtotal + total
            except:
                subtotal = subtotal 
        # if voucher:
        #     discount = voucher.coupon.discount
        #     if voucher.coupon.discount_type == 'PERCENTAGE':
        #         discount_amount = (discount/100) * subtotal
        #     else:
        #         discount_amount = discount
        return subtotal - discount_amount

    def is_credited(self,payable_amount,paid_amount):
        credited_amount = float(payable_amount) - float(paid_amount) 
        if credited_amount > 0:
            return True
        else :
            return False
#fix it
    def credited_amount(self, payable_amount, paid_amount):
        return round(float(payable_amount) - float(paid_amount), 6) 
        

    def to_representation(self, request=None):
        return {
            'id': self.id,
            'is_manual': self.is_manual,
            'invoice_number': self.invoice_number,
            'payment_mode': self.payment_mode,
            'service_charge': self.service_charge if self.is_service_charge else 0,
            'tax': self.tax,
            'subtotal': self.get_subtotal(),
            'grand_total': self.get_grand_total(),
            'company': self.company.to_representation(),
            'custom_discount_percentage': self.custom_discount_percentage,
            'custom_discount_amount': self.custom_discount_amount,
            'is_credit':self.is_credit,
            'is_paid':self.is_paid,

        }
    
    def order_representation(self, request=None):
        return {
            'id': self.id,
            'is_manual': self.is_manual,
            'invoice_number': self.invoice_number,
            'payment_mode': self.payment_mode,
            'service_charge': self.service_charge if self.is_service_charge else 0,
            'tax': self.tax,
            'subtotal': self.get_subtotal(),
            'grand_total': self.get_grand_total(),
            'custom_discount_percentage': self.custom_discount_percentage,
            'custom_discount_amount': self.custom_discount_amount,
            'is_credit':self.is_credit,
            'is_paid':self.is_paid,

        }


