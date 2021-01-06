from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from commonapp.models.order import Order, OrderLine
from notifications.constants import NOTIFICATION_CATEGORY, NOTIFICATION_CATEGORY_NAME
from notifications.models import Notification, NotificationCategory
from helpers.constants import ORDER_STATUS, ORDER_HEADER, ORDER_SCAN_COOLDOWN
from orderapp.models.order_scan_log import OrderScanLog
from helpers.exceptions import InvalidRequestException, OrderSessionExpiredException
from orderapp.serializers.order import TableOrderCreateSerializer


class OrderLineSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=False, allow_null=True)
    order = serializers.UUIDField(read_only=False, allow_null=True)
    product_name = serializers.SerializerMethodField()
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = OrderLine
        fields = ['id', 'product', 'product_name', 'product_code', 'rate', 'quantity','total','state', 'company', 'order']

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_code(self, obj):
        return obj.product.product_code

class OrderSaveSerializer(serializers.ModelSerializer):
    asset_name = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()
    order_lines = OrderLineSerializer(many=True, write_only=True)
    total = serializers.SerializerMethodField()
    taxed_amount = serializers.SerializerMethodField()
    service_charge = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def validate(self, attrs):
        asset = attrs.get('asset')
        company = attrs.get('company')
        order = None
        request = self.context.get('request')
        order = Order.objects.filter(
                            asset=asset,
                            company=company,
                            status__in=[ORDER_STATUS['NEW_ORDER'], ORDER_STATUS['CONFIRMED'], ORDER_STATUS['PROCESSING']]).exists()
        if not self.instance:
            if request:
                token = request.GET.get(ORDER_HEADER)
            if not token:
                raise InvalidRequestException()

            scan_validity = OrderScanLog.objects.filter(asset=asset, token=token).order_by('-created_at').first()
            is_session_valid = True
            if not scan_validity:
                is_session_valid = False
            else:
                scan_time = scan_validity.created_at
                current_time = timezone.now()
                time_diff = (current_time - scan_time).seconds
                if (ORDER_SCAN_COOLDOWN * 60) < time_diff:
                    is_session_valid = False
            if not is_session_valid:
                raise OrderSessionExpiredException()
            if order:
                raise ValidationError({'detail': 'Order is already in process for this asset.'})
        else:
            if not order:
                raise ValidationError({'detail': 'This Order cannot be updated. Please create a new order.'})

        return super(OrderSaveSerializer, self).validate(attrs)

    def prepare_new_table_order_data(self, validated_data, order_lines_data):
        new_line_data = list()
        for line in order_lines_data:
            new_line_data.append({
                'product': line['product'].id,
                'quantity': line['quantity']
            })
        return {
            'asset': validated_data.get('asset').id,
            'order_lines': new_line_data,
            'voucher': validated_data.get('voucher', None),
            'extras': {}
        }

    @transaction.atomic
    def create(self, validated_data):
        try:
            from notifications.tasks import notify_company_staffs
            order_lines_data = validated_data.pop('order_lines')
            order_obj = Order.objects.create(**validated_data)
            create_list = list()

            for order_lines in order_lines_data:
                order_lines['order'] = order_obj
                # OrderLine.objects.create(**order_lines)
                create_list.append(OrderLine(**order_lines))
            OrderLine.objects.bulk_create(create_list)

            new_order_data = self.prepare_new_table_order_data(validated_data, order_lines_data)
            new_order_data['extras']['legacy_order_id'] = order_obj.id
            request = self.context.get('request', {})

            setattr(request, 'company', order_obj.company)
            new_table_serializer = TableOrderCreateSerializer(data=new_order_data, context={'request': request})
            new_table_serializer.is_valid(raise_exception=True)
            new_table_serializer.save()
        except Exception as e:
            print("New order error")
            print(e)
            raise ValidationError({'detail': str(e)})
        ## sending notification to staffs  of associated company
        company = str(order_obj.company.id)
        payload = {
            'id': str(order_obj.id),
            'category': NOTIFICATION_CATEGORY_NAME['ORDER_PLACED'],
            'message': {
                'en': 'New order is placed from {0} {1}'.format(order_obj.asset.asset_type, order_obj.asset.name)
            }
        }
        notify_company_staffs.apply_async(kwargs={
                            'company': company,
                            'category': NOTIFICATION_CATEGORY['ORDER_PLACED'],
                            'payload': payload
                        })
        return order_obj

    def update(self, instance, validated_data):
        from notifications.tasks import notify_company_staffs
        order_lines_data = validated_data.pop('order_lines')
        order_lines_obj = OrderLine.objects.filter(order=instance.id)
        order_lines_ids = [str(x.id) for x in order_lines_obj]
        create_list = list()
        try:
            for order_lines in order_lines_data:
                order_line_id = str(order_lines.get('id'))
                if order_line_id in order_lines_ids:
                    OrderLine.objects.filter(id=order_line_id).update(**order_lines)
                    order_lines_ids.remove(order_line_id)
                else:
                    # order_obj = Order.objects.get(id=order_lines.pop('order'))
                    # order_lines.pop('id')
                    order_lines.pop('order')
                    create_list.append(OrderLine(order=instance, **order_lines))
                    # OrderLine.objects.create(order=instance, **order_lines)

            OrderLine.objects.bulk_create(create_list)
            OrderLine.objects.filter(id__in=order_lines_ids).delete()
            order_obj = Order.objects.filter(id=instance.id).update(**validated_data)
        except Exception as e:
            raise ValidationError({'detail': str(e)})
        ## sending notification to staffs  of associated company
        company = str(instance.company.id)
        payload = {
            'id': str(instance.id),
            'category': NOTIFICATION_CATEGORY_NAME['ORDER_UPDATED'],
            'message': {
                'en': 'Order has been updated from {0} {1}'.format(instance.asset.asset_type, instance.asset.name)
            }
        }
        notify_company_staffs.apply_async(kwargs={
                            'company': company,
                            'category': NOTIFICATION_CATEGORY['ORDER_UPDATED'],
                            'payload': payload
                        })
        return order_obj

    def get_asset_name(self, obj):
        return obj.asset.name

    def get_order(self, obj):
        order_lines_obj = OrderLine.objects.filter(order__id=obj.id)
        serializer = OrderLineSerializer(order_lines_obj, many=True)
        return serializer.data

    def get_total(self, obj):
        order_lines_obj = OrderLine.objects.filter(order=obj.id)
        total = 0
        for order_lines in order_lines_obj:
            total += order_lines.subtotal
        return float(total)

    def get_taxed_amount(self, obj):
        if obj.company.tax:
            total = self.get_total(obj)
            taxed_amount = float(obj.company.tax) / 100 * total
        else:
            taxed_amount = 0
        return float(taxed_amount)

    def get_service_charge(self, obj):
        if obj.company.service_charge:
            total = self.get_total(obj)
            service_charge = float(obj.company.service_charge) / 100 * total
        else:
            service_charge = 0
        return float(service_charge)

    def get_grand_total(self, obj):
        return float(self.get_total(obj) + self.get_taxed_amount(obj) + self.get_service_charge(obj))

class OrderSerializer(serializers.ModelSerializer):
    asset_name = serializers.SerializerMethodField()
    order_lines = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    taxed_amount = serializers.SerializerMethodField()
    service_charge = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_asset_name(self, obj):
        return obj.asset.name

    def get_order_lines(self, obj):
        order_lines_obj = OrderLine.objects.filter(order__id=obj.id)
        serializer = OrderLineSerializer(order_lines_obj, many=True)
        return serializer.data

    def get_total(self, obj):
        order_lines_obj = OrderLine.objects.filter(order=obj.id)
        total = 0
        for order_lines in order_lines_obj:
            total += order_lines.subtotal
        return float(total)

    def get_taxed_amount(self, obj):
        if obj.company.tax:
            total = self.get_total(obj)
            taxed_amount = float(obj.company.tax) / 100 * total
        else:
            taxed_amount = 0
        return float(taxed_amount)

    def get_service_charge(self, obj):
        if obj.company.service_charge:
            total = self.get_total(obj)
            service_charge = float(obj.company.service_charge) / 100 * total
        else:
            service_charge = 0
        return float(service_charge)

    def get_grand_total(self, obj):
        return float(self.get_total(obj) + self.get_taxed_amount(obj) + self.get_service_charge(obj))
