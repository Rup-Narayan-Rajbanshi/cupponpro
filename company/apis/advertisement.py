from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from company.serializers.advertisement import AdvertisementSerializer
from company.models.advertisement import Advertisement
from helpers.api_mixins import FAPIMixin
from helpers.paginations import FPagination
from rest_framework.permissions import AllowAny


class AdvertisementAPI(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Advertisement.objects.all().order_by('-created_at')
    serializer_class = AdvertisementSerializer
    pagination_class = FPagination
    permission_classes = (AllowAny, )