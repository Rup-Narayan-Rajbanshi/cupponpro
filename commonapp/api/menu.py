from rest_framework.response import Response
from rest_framework import generics
from commonapp.models.company import Company
from commonapp.serializers.menu import MenuSerializer
from permission import publicReadOnly

class MenuListView(generics.GenericAPIView):
    permission_classes = (publicReadOnly, )
    serializer_class = MenuSerializer

    def get(self, request, company_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            serializer = MenuSerializer(company_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exists."
            }
            return Response(data, status=404)