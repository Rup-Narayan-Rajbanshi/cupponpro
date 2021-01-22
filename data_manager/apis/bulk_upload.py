from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from data_manager.serializers.product_upload import UploadExcelProductSerializer
from data_manager.serializers.product_category_upload import UploadExcelProductCategorySerializer
from permission import CompanyUserPermission


@api_view(["POST"])
@permission_classes((CompanyUserPermission,))
@renderer_classes([JSONRenderer])
def product_data_upload(request):
    data = {"upload_file": request.data.get('upload_file')}
    serializer = UploadExcelProductSerializer(
        data=data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save(serializer.validated_data)
    return Response(
        {"detail": "Successfully uploaded product data from the excel sheet"},
        status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((CompanyUserPermission,))
@renderer_classes([JSONRenderer])
def product_category_data_upload(request):
    data = {"upload_file": request.data.get('upload_file')}
    serializer = UploadExcelProductCategorySerializer(
        data=data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save(serializer.validated_data)
    return Response(
        {"detail": "Successfully uploaded product category data from the excel sheet"},
        status=status.HTTP_200_OK)
