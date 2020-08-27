from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from articleapp.serializers.news import NewsArticleSerializer
from articleapp.models.news import NewsArticle
from permission import isAdminOrReadOnly

class NewsArticleListView(APIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = NewsArticleSerializer

    def get(self, request):
        news_obj = NewsArticle.objects.all().order_by('-id')
        paginator = Paginator(news_obj, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = NewsArticleSerializer(page_obj, many=True, context={'request':request})
        data = {
            'success': 1,
            'news_article': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        serializer = NewsArticleSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'news_article': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)

class NewsArticleDetailView(APIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = NewsArticleSerializer

    def get(self, request, news_id):
        news_obj = NewsArticle.objects.filter(id=news_id)
        if news_obj:
            serializer = NewsArticleSerializer(news_obj[0], context={'request':request})
            data = {
                'success': 1,
                'news_article': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'News article not found.'
            }
            return Response(data, status=400)

    def put(self, request, news_id):
        news_obj = NewsArticle.objects.filter(id=news_id)
        if news_obj:
            serializer = NewsArticleSerializer(instance=news_obj[0], data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'news_article': serializer.data
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': 'News article not found.'
            }
            return Response(data, status=400)

    def delete(self, request, news_id):
        news_obj = NewsArticle.objects.filter(id=news_id)
        if news_obj:
            news_obj[0].delete()
            data = {
                'success': 1,
                'news_article': 'News article deleted successfully.'
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'News article not found.'
            }
            return Response(data, status=400)
