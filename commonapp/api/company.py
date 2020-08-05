from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from commonapp.serializers.company import CompanySerializer, CompanyInfoSerializer
from commonapp.models.company import Company, CompanyInfo
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

class CompanyInfoListView(APIView):
    permission_classes = (Permission ,)
    serializer_class = CompanyInfoSerializer

    def get(self, request, company_id):
        company_info_obj = CompanyInfo.objects.filter(company=company_id)
        if company_info_obj:
            serializer = CompanyInfoSerializer(company_info_obj, many=True,\
                context={"request":request})
            data = {
                'success' : 1,
                'companyinfo' : serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success' : 0,
                "message" : "Companyinfo id not found."
            }
            return Response(data, status=404)