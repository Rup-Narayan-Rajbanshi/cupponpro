from rest_framework import serializers
from helpers.serializer import CustomModelSerializer
from commonapp.serializers.company import CompanySerializer
from helpers.serializer_fields import ImageFieldWithURL
from company.models.partner import Partner, DeliveryPartner



class PartnerSerializer(CustomModelSerializer):
    logo = ImageFieldWithURL()

    class Meta(CustomModelSerializer.Meta):
        model = Partner




class DeliveryPartnerSerializer(CustomModelSerializer):
    logo = ImageFieldWithURL()

    class Meta(CustomModelSerializer.Meta):
        model = DeliveryPartner

    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            try:
                company_user = request.user.company_user.all()
                company = company_user[0].company
            except:
                company = None
            if company:
                attrs['company'] = company
        return attrs

