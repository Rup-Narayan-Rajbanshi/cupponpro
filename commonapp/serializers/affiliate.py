from django.contrib.sites.models import Site
from rest_framework import serializers
from commonapp.models.affiliate import AffiliateLink
from helpers.serializer_fields import ImageFieldWithURL


class AffiliateLinkSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()
    image = ImageFieldWithURL(allow_empty_file=True)

    class Meta:
        model = AffiliateLink
        fields = "__all__"

    def get_vendor(self, obj):
        try:
            current_site = Site.objects.get_current()
            logo = current_site.domain + obj.company.logo.url
        except:
            logo = None
        data = {
            'id': obj.company.id,
            'name': obj.company.name,
            'logo': logo
        }
        return data

class AffiliateLinkDetailSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()
    image = ImageFieldWithURL(allow_empty_file=True)

    class Meta:
        model = AffiliateLink
        fields = ('id', 'url', 'discount_code', 'image', 'description', 'discount', 'vendor')

    def get_vendor(self, obj):
        try:
            current_site = Site.objects.get_current()
            logo = current_site.domain + obj.company.logo.url
        except:
            logo = None
        data = {
            'id': obj.company.id,
            'name': obj.company.name,
            'logo': logo
        }
        return data

    def exclude_fields(self, fields_to_exclude=None):
        if isinstance(fields_to_exclude, list):
            for f in fields_to_exclude:
                f in self.fields.fields and self.fields.fields.pop(f) or next()
