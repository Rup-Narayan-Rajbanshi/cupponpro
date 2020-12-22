from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from data_manager.serializers.bulk_upload import UploadExcelProductSerializer
from permission import CompanyUserPermission


@api_view(["POST"])
@permission_classes((CompanyUserPermission,))
@renderer_classes([JSONRenderer])
def customer_data_upload(request):
    data = {"upload_file": request.data.get('upload_file')}
    serializer = UploadExcelProductSerializer(
        data=data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save(serializer.validated_data)
    return Response(
        {"detail": "Successfully uploaded customer data from the excel sheet"},
        status=status.HTTP_200_OK)

