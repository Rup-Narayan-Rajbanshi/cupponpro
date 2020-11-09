from rest_framework import serializers
from commonapp.models.company import Company
from commonapp.models.product import Product, ProductCategory
from commonapp.models.order import Order
from commonapp.serializers.order import OrderSerializer
from commonapp.serializers.image import ImageDetailSerializer

class MenuSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField()
    images = ImageDetailSerializer(many=True, read_only=True)
    order = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('id', 'name', 'service_charge', 'tax', 'currency', 'logo', 'images', 'menu', 'order')

    def get_menu(self, obj):
        data = list()
        product_category_obj = ProductCategory.objects.filter(company=obj.id)
        for product_category in product_category_obj:
            menu = dict()
            menu['category_name'] = product_category.name
            products = list()
            product_obj = Product.objects.filter(product_category=product_category)
            for each_product in product_obj:
                product = dict()
                product['id'] = each_product.id
                product['name'] = each_product.name
                product['price'] = each_product.total_price
                products.append(product)
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
