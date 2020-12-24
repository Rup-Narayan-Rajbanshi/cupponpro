from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from commonapp.models.asset import Asset
from commonapp.serializers.asset import AssetSerializer
from helper import isCompanyUser
from permission import isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll, publicReadOnly
from commonapp.app_helper import custom_paginator


class AssetListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | publicReadOnly]
    serializer_class = AssetSerializer

    def get(self, request, company_id):
        """
        An endpoint for listing all the vendor's asset. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        asset_obj = Asset.objects.filter(company=company_id)
        data = custom_paginator(request=request,
                        queryset=asset_obj,
                        serializer=AssetSerializer
                    )
        return Response(data, status=200)

    def post(self, request, company_id):
        """
        An endpoint for creating vendor's asset.
        """
        if isCompanyUser(request.user.id, company_id):
            serializer = AssetSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'data': serializer.data
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "You don't have permission to add an asset."
            }
            return Response(data, status=403)

class AssetDetailView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = AssetSerializer

    def get(self, request, company_id, asset_id):
        """
        An endpoint for getting vendor's asset detail.
        """
        asset_obj = Asset.objects.filter(id=asset_id, company=company_id)
        if asset_obj:
            serializer = AssetSerializer(asset_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'message': "Asset doesn't exist.",
            }
            return Response(data, status=404)

    def put(self, request, company_id, asset_id):
        """
        An endpoint for updating vendor's asset.
        """
        if isCompanyUser(request.user.id, company_id):
            asset_obj = Asset.objects.filter(id=asset_id, company=company_id)
            serializer = AssetSerializer(instance=asset_obj[0], data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'data': serializer.data
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "You don't have permission to update an asset."
            }
            return Response(data, status=403)

    def delete(self, request, company_id, asset_id):
        """
        An endpoint for deleting vendor's asset.
        """
        asset_obj = Asset.objects.filter(id=asset_id, company=company_id)
        if asset_obj:
            try:
                asset_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': 'Asset cannot be deleted.'
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Asset doesn't exist."
            }
            return Response(data, status=404)
