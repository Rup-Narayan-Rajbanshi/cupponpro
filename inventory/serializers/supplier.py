from rest_framework import serializers
from helpers.serializer import CustomModelSerializer
from inventory.models.supplier import Supplier
from rest_framework.exceptions import ValidationError
from company.models.company import Company
from helpers.serializer_fields import DetailRelatedField


class SupplierSerializer(CustomModelSerializer):
    name = serializers.CharField(max_length=64)
    company = DetailRelatedField(model=Company, lookup='id', representation='inventory_representation', required=False, allow_null=True)



    class Meta:
        model = Supplier
        fields = '__all__'

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
        return attrs