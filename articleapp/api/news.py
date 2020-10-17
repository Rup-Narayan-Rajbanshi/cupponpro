from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from articleapp.serializers.news import NewsArticleSerializer
from articleapp.models.news import NewsArticle
from permission import isAdminOrReadOnly

class NewsArticleListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = NewsArticleSerializer

    def get(self, request):
        """
        An endpoint for listing all the news. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        news_obj = NewsArticle.objects.all().order_by('-id')
        paginator = Paginator(news_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = NewsArticleSerializer(page_obj, many=True, context={'request':request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        """
        An endpoint for creating news.
        """
        serializer = NewsArticleSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)

class NewsArticleDetailView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = NewsArticleSerializer

    def get(self, request, news_id):
        """
        An endpoint for getting news detail.
        """
        news_obj = NewsArticle.objects.filter(id=news_id)
        if news_obj:
            serializer = NewsArticleSerializer(news_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'News article not found.'
            }
            return Response(data, status=404)

    def put(self, request, news_id):
        """
        An endpoint for updating news detail.
        """
        news_obj = NewsArticle.objects.filter(id=news_id)
        if news_obj:
            serializer = NewsArticleSerializer(instance=news_obj[0], data=request.data,\
                partial=True, context={'request':request})
            if 'image' in request.data and not request.data['image']:
                serializer.exclude_fields(['image'])
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'data': serializer.data
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
            return Response(data, status=404)

    def delete(self, request, news_id):
        """
        An endpoint for deleting news.
        """
        news_obj = NewsArticle.objects.filter(id=news_id)
        if news_obj:
            try:
                news_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': 'News article cannot be deleted.'
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': 'News article not found.'
            }
            return Response(data, status=404)
