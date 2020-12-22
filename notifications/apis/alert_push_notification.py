from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from commonapp.models.company import Company
from notifications.models import Device
from notifications.tasks import notify_company_staffs


@api_view(["POST"])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated,))
def send_table_alert_notification(request, company_id):
    company = Company.objects.filter(id=company_id)[0]
    payload = {
        'message': 'Pending order'
    }
    notify_company_staffs(company, 1, payload)
    return Response({"detail": "Successfully notified"}, status=status.HTTP_200_OK)
