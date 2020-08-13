from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from billapp.serializers.bill import BillSerializer
from billapp.models.bill import Bill
from permission import Permission

class BillListView(APIView):
    permission_classes = (Permission ,)
    serializer_class = BillSerializer

    def get(self, request):
        bill_obj = Bill.objects.all()
        serializer = BillSerializer(bill_obj, many=True,\
            context={'request':request})
        data = {
            'success': 1,
            'bill': serializer.data,
        }
        return Response(data, status=200)
    
    def post(self,request):
        if request.user.admin:
            serializer = BillSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'bill': serializer.data,
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.error,
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to add a banner."
        }
        return Response(data, status=403)