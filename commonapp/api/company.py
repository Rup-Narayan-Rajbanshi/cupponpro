from rest_framework.views import APIView
from rest_framework.response import Response
from commonapp.serializers.company import CompanySerializer
from commonapp.models.company import Company
from permission import Permission
from rest_framework.permissions import AllowAny

class CompanyListView(APIView):
    permission_classes = (Permission ,)
    serializer_class = CompanySerializer

    def get(self, request):
        company_obj = Company.objects.all()
        serializer = CompanySerializer(company_obj, many=True,\
            context={"request":request})
        data = {
            'success' : 1,
            'company' : serializer.data,
        }
        return Response(data, status=200)

class PartnerListView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = CompanySerializer

    def get(self, request):
        company_obj = Company.objects.filter(is_partner=True).order_by('-id')
        serializer = CompanySerializer(company_obj, many=True,\
            context={"request":request})
        data = {
            'success' : 1,
            'company' : serializer.data,
        }
        return Response(data, status=200)