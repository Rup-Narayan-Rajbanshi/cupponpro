from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from helpers.serializer_fields import DetailRelatedField
from company.models.rating import Rating
from company.models.company import Company


class RatingSerializer(serializers.ModelSerializer):
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation', read_only=True)

    class Meta:
        model = Rating
        fields = "__all__"
        write_only_fields = ('created_at',)

    def validate(self, attrs):
        company_id = self.context.get('company_id', None)
        try:
            self.company = Company.objects.get(id=company_id)
        except ObjectDoesNotExist:
            raise ValidationError({'company_id': 'Object does not exist.'})
        return attrs

    def create(self, validated_data):
        validated_data['company'] = self.company
        return super(RatingSerializer, self).create(validated_data)
