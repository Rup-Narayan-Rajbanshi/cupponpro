from rest_framework.viewsets import GenericViewSet, mixins
from helpers.paginations import FPagination
from rest_framework.permissions import IsAuthenticated
from helpers.api_mixins import FAPIMixin
from company.models.follow import Follows
from company.models.likes import Like
from company.serializers.follow import FollowSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class FollowAPI(FAPIMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Follows.objects.select_related('company', 'user').all().order_by('created_at')
    pagination_class = FPagination
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request:
            is_admin = self.request.user.group.filter(name='admin').exists()
            if is_admin:
                queryset = Follows.objects.all().order_by('created_at')
                return queryset
            user = self.request.user
            user_from_params = self.request.query_params.get('user', None)
            if user_from_params:
                user = user_from_params
            try:
                company_logged_in = self.request.user.company_user.all().values_list('company', flat=True)[0]
            except:
                company_logged_in = None 
            if company_logged_in:
                queryset = Follows.objects.filter(company = company_logged_in).order_by('created_at')
                return queryset
            # company = self.request.query_params.get('company', None)
            # if company:
            #     queryset = Follows.objects.filter(user = user, company=company)
            #     return queryset
            queryset = Follows.objects.filter(user = user).order_by('created_at')
            return queryset


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            data={
                'success': 1,
                'message': 'Unfollowed'
            }
            return Response(data, status=200)
        else:
            data={
                'success': 0,
                'message': 'Cannot unfollow.'
            }
            return Response(data, status=200)

class GetLikeAndFollowAPI(FAPIMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Follows.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]


    def list(self, request, *args , **kwargs):
        company = request.query_params.get('company', None)
        user = request.user
        user_from_params = self.request.query_params.get('user', None)
        if user_from_params:
            user = user_from_params
        data = dict()
        if company:
            follow_query = Follows.objects.filter(company=company, user=user)
            like_query = Like.objects.filter(company=company, user=user)
            if like_query:
                data['like_status'] = True
                data['like_id'] = like_query[0].id
            else:
                data['like_status'] = False
                data['like_id'] = None
            if follow_query:
                data['follow_status'] = True
                data['follow_id'] = follow_query[0].id
            else:
                data['follow_status'] = False
                data['follow_id'] = None
        return Response(data, status=200)
    