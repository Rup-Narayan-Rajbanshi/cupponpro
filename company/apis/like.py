from rest_framework.viewsets import GenericViewSet, mixins
from helpers.paginations import FPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from helpers.api_mixins import FAPIMixin
from company.models.likes import Like
from company.filters import CompanyLikeBaseFilter, LikeFilter
from company.serializers.like import LikeSerializer
from rest_framework.response import Response

class CompanyLikeAPI(FAPIMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Like.objects.select_related('company', 'user').all()
    serializer_class = LikeSerializer
    filter_class = LikeFilter
    pagination_class = FPagination
    permission_classes = (IsAuthenticated,   )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            data={
                'success': 1,
                'message': 'Unliked'
            }
            return Response(data, status=200)
        else:
            data={
                'success': 0,
                'message': 'Like Object does not exist'
            }
            return Response(data, status=200)
    