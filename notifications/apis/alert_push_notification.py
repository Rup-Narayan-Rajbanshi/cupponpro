from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from commonapp.models.asset import Asset
from notifications.constants import NOTIFICATION_CATEGORY_NAME, NOTIFICATION_CATEGORY
from notifications.tasks import notify_company_staffs


@api_view(["POST"])
@renderer_classes([JSONRenderer])
@permission_classes((AllowAny,))
def send_table_alert_notification(request, asset_id):
    type = request.GET.get('type')
    payload = dict()
    asset = Asset.objects.filter(id=asset_id).first()
    if asset and (type in ['BILL', 'ALERT']):
        if type == 'BILL':
            payload = {
                'category': NOTIFICATION_CATEGORY_NAME['ORDER_PAYMENT'],
                'message': {
                    'en': 'Bill requested from {0} {1}'.format(asset.asset_type, asset.name)
                }
            }
        elif type == 'ALERT':
            payload = {
                'category': NOTIFICATION_CATEGORY_NAME['ORDER_PLACED'],
                'message': {
                    'en': 'Waiter requested from {0} {1}'.format(asset.asset_type, asset.name)
                }
            }

        notify_company_staffs.apply_async(kwargs={
            'company': asset.company,
            'category': NOTIFICATION_CATEGORY['ORDER_PLACED'],
            'payload': payload
        })
        return Response({"detail": "Successfully notified"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Unable to find asset"}, status=status.HTTP_400_BAD_REQUEST)
