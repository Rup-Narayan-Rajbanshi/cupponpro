from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from articleapp.serializers.blogs import BlogSerializer
from articleapp.models.blogs import Blog
from helpers.api_mixins import FAPIMixin
from helpers.paginations import FPagination
from rest_framework.permissions import AllowAny


class BlogAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    pagination_class = FPagination
    permission_classes = (AllowAny, )