from rest_framework.response import Response
from rest_framework import generics
from company.models.company import Company
from commonapp.serializers.menu import MenuSerializer
from permission import publicReadOnly

class MenuListView(generics.GenericAPIView):
    permission_classes = (publicReadOnly, )
    serializer_class = MenuSerializer

    def get(self, request, company_id):
        """
        An endpoint to list the necessary company detail and menu. Pass asset id as query parameter in 'asset' to get order detail as well.
        """
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