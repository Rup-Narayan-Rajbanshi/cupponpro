from rest_framework import serializers
from helpers.serializer_fields import DetailRelatedField
from helpers.serializer_fields import ImageFieldWithURL
from commonapp.models.category import Category, SubCategory
from company.models.company import Company, FavouriteCompany
from company.models.links import SocialLink
from company.models.rating import Rating
from commonapp.serializers.image import ImageDetailSerializer
from commonapp.serializers.links import SocialLinkSerializer
from userapp.models.user import User


class CompanySerializer(serializers.ModelSerializer):
    logo = ImageFieldWithURL(allow_empty_file=True)
    logo_icon = ImageFieldWithURL(allow_empty_file=True)
    images = ImageDetailSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Company
        exclude = ('key', 'created_at')
        # fields = "__all__"

    def get_rating(self, obj):
        # rating_obj = Rating.objects.filter(company=obj.id)
        # rating_count = len(rating_obj)
        # rating = 0
        # if rating_obj:
        #     for each_rating_obj in rating_obj:
        #         rating += each_rating_obj.rate
        #     rating /= rating_count
        rating = obj.rating if getattr(obj, 'rating', None) else 0
        return rating

    def get_rating_count(self, obj):
        rating_count = obj.rating_count if getattr(obj, 'rating_count', None) else 0
        return rating_count
        # return Rating.objects.filter(company=obj.id).count()

    def get_links(self, obj):
        social_link_obj = SocialLink.objects.filter(company=obj.id)
        serializer = SocialLinkSerializer(social_link_obj, many=True)
        return serializer.data

    def exclude_fields(self, fields_to_exclude=None):
        if isinstance(fields_to_exclude, list):
            for f in fields_to_exclude:
                f in self.fields.fields and self.fields.fields.pop(f) or next()


class ChangeCompanyEmailSerializer(serializers.Serializer):
    """
    Serializer for company's email change endpoint.
    """
    model = Company

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class FavouriteCompanySerializer(serializers.ModelSerializer):
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation', read_only=True)
    user = DetailRelatedField(model=User, lookup='id', representation='to_representation', read_only=True)
    is_favourite = serializers.BooleanField()

    class Meta:
        model = FavouriteCompany
        fields = "__all__"

    def update(self, instance, vdata):
        # user = self.context.get('request').user
        # vdata['user'] = user
        for attr, value in vdata.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
