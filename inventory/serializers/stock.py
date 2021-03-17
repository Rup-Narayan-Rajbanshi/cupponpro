from rest_framework import serializers
from helpers.serializer import CustomModelSerializer
from inventory.models.stock import Stock
from rest_framework.exceptions import ValidationError
from helpers.serializer_fields import DetailRelatedField
from django.db import transaction
from notifications.constants import NOTIFICATION_CATEGORY_NAME, NOTIFICATION_CATEGORY
from commonapp.models.company import Company



class StockSerializer(CustomModelSerializer):
    name = serializers.CharField(max_length=64)
    company = DetailRelatedField(model=Company, lookup='id', representation='inventory_representation', required=False, allow_null=True)


    class Meta:
        model = Stock
        fields = "__all__"

    
    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            try:
                company_user = request.user.company_user.all()
                company = company_user[0].company
            except:
                company=None
            print(company)
            if company:
                attrs['company'] = company
            name = attrs.get('name', None)
            if name:
                if not self.instance:
                    is_name = Stock.objects.filter(name=name, company=company).exists()
                    if is_name:
                        raise ValidationError({'name':'Name already exists'})
                else:
                    if not self.instance.name == name:
                        is_name = Stock.objects.filter(name=name, company=company).exists()
                        if is_name:
                            raise ValidationError({'name':'Name already exists'})
        return attrs

