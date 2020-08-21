from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from billapp.serializers.salesitem import SalesitemSerializer
from billapp.models.salesitem import Salesitem
from permission import isCompanyOwner, isCompanyManager

class SalesitemListView(APIView):
    permission_classes = (isCompanyOwner, isCompanyManager, )
    serializer_class = SalesitemSerializer

    def get(self, request, bill_id):
        salesitem_obj = Salesitem.objects.filter(bill__id = bill_id)
        if salesitem_obj:
            serializer = SalesitemSerializer(salesitem_obj, many=True,\
                context={'request':request})
            data = {
                'success': 1,
                'sales_item': serializer.data,
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'Sales item not found.',
            }
            return Response(data, status=400)
    
    def post(self, request, bill_id):
        if int(request.data['bill']) == bill_id:
            serializer = SalesitemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'salesitem': serializer.data,
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializers.errors,
            }
            return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': 'Sales item cannot be created',
            }
            return Response(data, status=400)