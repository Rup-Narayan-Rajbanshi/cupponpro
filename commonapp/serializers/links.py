from rest_framework import serializers
from company.models.links import SocialLink

class SocialLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialLink
        fields = '__all__'