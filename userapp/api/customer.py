from userapp.models.customer import Customer
from rest_framework.viewsets import ModelViewSet, generics
from userapp.serializers.customer import CustomerSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from helpers.paginations import FPagination

class CustomerAPI(ModelViewSet):
    queryset = Customer.objects.all().order_by('name')
    serializer_class = CustomerSerializer
    pagination_class = FPagination
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class CustomerFromPhone(generics.GenericAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny, )

    def get(self, request):
        status = 200
        phone_number = request.query_params.get('phone_number')
        if Customer.objects.filter(phone_number=phone_number):
            customer = Customer.objects.get(phone_number=phone_number)
            serializer = CustomerSerializer(customer, context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
        else:
            status = 403
            data = {
                'success': 0,
                'message': 'Customer does not exist. '
            }
        return Response(data, status=status)