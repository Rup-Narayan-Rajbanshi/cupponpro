from rest_framework import serializers
from helpers.serializer_fields import ImageFieldWithURL
from productapp.models.product import BulkQuantity, Product, ProductCategory
from commonapp.serializers.image import ImageDetailSerializer
from helpers.choices_variable import CURRENCY_TYPE_CHOICES, PRODUCT_STATUS_CHOICES, PRODUCT_TYPE_CHOICES
from helpers.serializer import CustomModelSerializer

class BulkQuantitySerializer(CustomModelSerializer):

    class Meta:
        model = BulkQuantity
        fields = "__all__"

class ProductCategorySerializer(CustomModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=False)
    
    class Meta:
        model = ProductCategory
        fields = "__all__"

class ProductSerializer(CustomModelSerializer):
    images = ImageDetailSerializer(many=True, read_only=True)
    purchase_currency = serializers.ChoiceField(CURRENCY_TYPE_CHOICES, required=False)
    selling_currency = serializers.ChoiceField(CURRENCY_TYPE_CHOICES, required=False)
    status = serializers.ChoiceField(PRODUCT_STATUS_CHOICES)
    types = serializers.ChoiceField(PRODUCT_TYPE_CHOICES, allow_blank=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"


    # def validate(self, attrs):
    #     print(attrs)
    #     tags = attrs.get('tag')
    #     print(tags)


        # content_type = attrs.get('content_type')
        # object_id = attrs.get('object_id')
        # request = self.context.get('request')
        # if request:
        #     try:
        #         company_user = request.user.company_user.all()
        #         company = company_user[0].company
        #     except:
        #         company = None
        #     if company:
        #         attrs['company'] = company
        
        # if content_type and object_id:
        #     content_class = content_type.model_class()
        #     try:
        #         object = content_class.objects.get(id=object_id)
        #     except ObjectDoesNotExist:
        #         raise ValidationError({'object_id': 'Object does not exist.'})
        # return attrs

