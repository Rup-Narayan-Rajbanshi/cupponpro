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

    def get(self, request):
        company_info_obj = CompanyInfo.objects.all()
        serializer = CompanyInfoSerializer(company_info_obj, many=True,\
            context={"request":request})
        data = {
            'success' : 1,
            'companyinfo' : serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        if request.user.admin:
            serializer = CompanyInfoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'companyinfo': serializer.data,
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors,
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to add a companyinfo."
        }
        return Response(data, status=403)

class  CompanyInfoDetailView(APIView):
    permission_classes = (Permission, )
    serializer_class = CompanyInfoSerializer

    def get(self, request, companyinfo_id):
        if CompanyInfo.objects.filter(id=companyinfo_id):
            company_info_obj = CompanyInfo.objects.get(id=companyinfo_id)
            serializer = CompanyInfoSerializer(company_info_obj,\
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

    def put(self, request, companyinfo_id):
        if request.user.admin:
            if CompanyInfo.objects.filter(id=companyinfo_id):
                company_info_obj = CompanyInfo.objects.get(id=companyinfo_id)
                serializer = CompanyInfoSerializer(instance=company_info_obj,\
                    data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success': 1,
                        'companyinfo': serializer.data
                    }
                    return Response(data, status=200)
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
            data = {
                'success': 0,
                'message': "Companyinfo id not found."
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to update companyinfo."
        }
        return Response(data, status=403)

    def delete(self, request, companyinfo_id):
        if request.user.admin:
            if CompanyInfo.objects.filter(id=companyinfo_id):
                company_info_obj = CompanyInfo.objects.get(id=companyinfo_id)
                company_info_obj.delete()
                data = {
                    'success': 1,
                    'banner': "Companyinfo deleted successfully."
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': "Companyinfo id not found."
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to delete companyinfo."
        }
        return Response(data, status=403)