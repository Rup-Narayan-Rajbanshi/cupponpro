from rest_framework import serializers
from commonapp.models.affiliate import AffiliateLink

class AffiliateLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = AffiliateLink
        fields = "__all__"
    
    def exclude_fields(self, fields_to_exclude=None):
        if isinstance(fields_to_exclude, list):
            for f in fields_to_exclude:
                f in self.fields.fields and self.fields.fields.pop(f) or next()