from rest_framework import serializers
from helpers.serializer_fields import ImageFieldWithURL
from commonapp.models.company import Company
from productapp.models.product import Product, ProductCategory
from commonapp.models.order import Order
from commonapp.models.asset import Asset
from commonapp.serializers.order import OrderSerializer
from commonapp.serializers.image import ImageDetailSerializer

class MenuProductSerializer(serializers.ModelSerializer):
    images = ImageDetailSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id', 'name', 'product_code', 'price', 'images')

    def get_price(self, obj):
        return obj.total_price

class MenuSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField()
    asset = serializers.SerializerMethodField()
    images = ImageDetailSerializer(many=True, read_only=True)
    order = serializers.SerializerMethodField()
    logo = ImageFieldWithURL(allow_empty_file=True)
    logo_icon = ImageFieldWithURL(allow_empty_file=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'service_charge', 'tax', 'currency', 'logo', 'logo_icon', 'asset', 'images', 'menu', 'order')

    def get_asset(self, obj):
        request = self.context.get('request', None)
        asset = None
        if request:
            asset_id = request.GET.get('asset')
            try:
                asset = Asset.objects.get(id=asset_id)
                asset = asset.to_representation()
            except Exception as e:
                pass
        return asset

    def get_menu(self, obj):
        data = list()
        request = self.context.get('request', None)
        name = request.GET.get('name') if request else ''
        product_category_obj = ProductCategory.objects.filter(company=obj.id).order_by('position','name')
        if name:
            product_category_obj = product_category_obj.filter(product__name__istartswith=name)
        for product_category in product_category_obj:
            menu = dict()
            menu['category_name'] = product_category.name
            products = list()
            product_obj = Product.objects.filter(product_category=product_category, status='ACTIVE').order_by('name')
            if name:
                product_obj = product_obj.filter(name__istartswith=name)
            for each_product in product_obj:
                serializers = MenuProductSerializer(each_product, context={'request':self.context['request']})
                products.append(serializers.data)
            menu['products'] = products
            data.append(menu)
        return data

    def get_order(self, obj):
        asset_id = self.context['request'].GET.get('asset', None)
        order_obj = Order.objects.filter(asset=asset_id, is_billed=False)
        if order_obj:
            serializer = OrderSerializer(order_obj[0])
            return serializer.data
        else:
            return None
