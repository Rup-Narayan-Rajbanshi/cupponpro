from rest_framework.views import APIView
from rest_framework.response import Response
from commonapp.serializers.company import CompanySerializer
from commonapp.models.company import Company
from permission import Permission

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