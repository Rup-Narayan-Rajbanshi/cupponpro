from rest_framework import serializers
from commonapp.models.category import Category, SubCategory
from commonapp.models.company import Company, FavouriteCompany
from commonapp.models.rating import Rating
from commonapp.serializers.image import ImageSerializer
from userapp.models.user import User

class CompanySerializer(serializers.ModelSerializer):

    images = ImageSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        exclude = ('key',)
        # fields = "__all__"

    def get_rating(self, obj):
        rating_obj = Rating.objects.filter(company=obj.id)
        rating_count = len(rating_obj)
        rating = 0
        if rating_obj:
            for each_rating_obj in rating_obj:
                rating += each_rating_obj.rate
            rating /= rating_count
        return rating

    def get_rating_count(self, obj):
        return Rating.objects.filter(company=obj.id).count()

class FavouriteCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = FavouriteCompany
        fields = "__all__"
