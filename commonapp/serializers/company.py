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
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    
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

    def get_author(self, obj):
        return {
            'id': obj.author_id,
            'name': User.objects.get(id=obj.author_id).full_name
        }
    
    def get_category(self, obj):
        return {
            'id': obj.category_id,
            'name': Category.objects.get(id=obj.category_id).name
        }
    
    def get_sub_category(self, obj):
        if obj.sub_category_id:
            return {
                'id': obj.sub_category_id,
                'name': SubCategory.objects.get(id=obj.sub_category_id).name
            }
        else:
            return None

class FavouriteCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = FavouriteCompany
        fields = "__all__"
