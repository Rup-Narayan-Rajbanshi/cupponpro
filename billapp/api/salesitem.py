from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from billapp.serializers.salesitem import SalesitemSerializer
from billapp.models.salesitem import Salesitem
from permission import Permission

class SalesitemListView(APIView):
    permission_classes = (Permission ,)
    serializer_class = SalesitemSerializer

    def get(self, request):
        salesitem_obj = Salesitem.objects.all()
        serializer = SalesitemSerializer(salesitem_obj, many=True,\
            context={'request':request})
        data = {
            'success': 1,
            'banner': serializer.data,
        }
        return Response(data, status=200)
    
    def post(self, request):
        if request.user.admin:
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
        data = {
            'success': 0,
            'message': 'You do not have permission to add a banner.'
        }
        return Response(data, status=403)