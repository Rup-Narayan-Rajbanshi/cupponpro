from rest_framework import mixins, status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from orderapp.models.bills import Bills
from orderapp.models.order import Orders
from orderapp.serializers.bill import BillCreateSerializer, ManualBillSerializerCompany, BillListSerializer
from permission import CompanyUserPermission
from orderapp.filters import BillFilter


class BillCreateAPI(FAPIMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Bills.objects.all().order_by('-created_at')
    serializer_class = BillCreateSerializer
    permission_classes = (CompanyUserPermission, )

class BillAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Bills.objects.all().order_by('-created_at')
    serializer_class = BillListSerializer
    pagination_class = FPagination
    permission_classes = (CompanyUserPermission, )
    filter_class = BillFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            data={
                'success': 1,
                'message': 'Deleted one table order.'
            }
            return Response(data, status=200)
        else:
            data={
                'success': 0,
                'message': 'Bill does not exit.'
            }
            return Response(data, status=200)


class ManualBillCreateAPI(FAPIMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Orders.objects.all().order_by('-created_at')
    serializer_class = ManualBillSerializerCompany
    permission_classes = (CompanyUserPermission, )

    def create(self, request, *args, **kwargs):
        order = super().create(request, *args, **kwargs)
        return order

@api_view(["GET"])
@permission_classes((CompanyUserPermission,))
@renderer_classes([JSONRenderer])
def get_order_list(request, order_id):
    order = Orders.objects.filter(id=order_id).first()
    if order and order.bill:
        return Response(order.bill.to_representation(), status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_200_OK)
