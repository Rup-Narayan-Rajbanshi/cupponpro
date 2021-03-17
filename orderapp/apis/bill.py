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
from django.utils import timezone

class BIllUpdateAPI(FAPIMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Bills.objects.all().order_by('-created_at')
    serializer_class = BillCreateSerializer
    permission_classes = (CompanyUserPermission, )

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(BIllUpdateAPI, self).update(request, *args, **kwargs)

        

class BillCreateAPI(FAPIMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Bills.objects.all().order_by('-created_at')
    serializer_class = BillCreateSerializer
    permission_classes = (CompanyUserPermission, )



class BillAPI(FAPIMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Bills.objects.all().order_by('-created_at', 'is_paid')
    serializer_class = BillListSerializer
    pagination_class = FPagination
    permission_classes = (CompanyUserPermission, )
    filter_class = BillFilter

    def get_queryset(self):
        company = getattr(self.request, 'company', None)
        sort_by = self.request.query_params.get('sort_by', None)
        group = self.request.user.group.all().first().name
        if group == 'sales':
            if sort_by:
                order_by = self.request.query_params.get('order_by', 'desc')
                if order_by == 'asc':
                    queryset = Bills.objects.filter(company=company, created_at__date=timezone.now().date()).order_by(sort_by)
                else:
                    queryset = Bills.objects.filter(company=company, created_at__date=timezone.now().date()).order_by('-' + sort_by)
            else:
                queryset = Bills.objects.filter(company=company, created_at__date=timezone.now().date()).order_by('-created_at', 'is_paid')
        else:
            if sort_by:
                order_by = self.request.query_params.get('order_by', 'desc')
                if order_by == 'asc':
                    queryset = Bills.objects.filter(company=company).order_by(sort_by)
                else:
                    queryset = Bills.objects.filter(company=company).order_by('-' + sort_by)
            else:
                queryset = Bills.objects.filter(company=company).order_by('-created_at', 'is_paid')
        return queryset


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
    
    def create(self, request, *args, **kwargs):
        serializer = ManualBillSerializerCompany(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # order = super().create(request, *args, **kwargs)
        # return order

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        bill = self.get_object()
        order = Orders.objects.filter(bill=bill).first()
        serializer = ManualBillSerializerCompany(instance=order, data=request.data, context={'request':request}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
        


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
