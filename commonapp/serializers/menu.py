from rest_framework import serializers
from commonapp.models.company import Company
from commonapp.models.product import Product, ProductCategory

class MenuSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = ('id', 'name', 'menu', )
        # read_only_fields = ('name', )

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
