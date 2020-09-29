from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from bannerapp.serializers.banner import BannerSerializer
from bannerapp.models.banner import Banner
from permission import isAdminOrReadOnly

class BannerListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = BannerSerializer

    def get(self, request):
        """
        An endpoint for listing all the banners. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        banner_obj = Banner.objects.all().order_by('-id')
        paginator = Paginator(banner_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = BannerSerializer(page_obj, many=True,\
            context={"request":request})
        data = {
            'success': 1,
            'banner': serializer.data,
        }
        return Response(data, status=200)

    def post(self, request):
        """
        An endpoint for creating banner.
        """
        serializer = BannerSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'banner': serializer.data,
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors,
        }
        return Response(data, status=400)


class BannerUpdateView(generics.GenericAPIView):
    serializer_class = BannerSerializer
    permission_classes = (isAdminOrReadOnly, )

    def get(self, request, banner_id):
        """
        An endpoint for getting banner detail.
        """
        banner_obj = Banner.objects.filter(id=banner_id)
        if banner_obj:
            serializer = BannerSerializer(banner_obj[0],\
                context={'request': request})
            data = {
                'success': 1,
                'banner': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': "Banner doesn't exist."
        }
        return Response(data, status=404)

    def put(self, request, banner_id):
        """
        An endpoint for updating banner detail.
        """
        banner_obj = Banner.objects.filter(id=banner_id)
        if banner_obj:
            serializer = BannerSerializer(instance=banner_obj[0],\
                data=request.data, partial=True, context={'request':request})
            if 'image' in request.data and not request.data['image']:
                serializer.exclude_fields(['image'])
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'banner': serializer.data
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "Banner doesn't exist."
        }
        return Response(data, status=404)

    def delete(self, request, banner_id):
        """
        An endpoint for deleting banner.
        """
        banner_obj = Banner.objects.filter(id=banner_id)
        if banner_obj:
            try:
                banner_obj[0].delete()
                data = {
                    'success': 1,
                    'banner': "Banner deleted successfully."
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': 'Banner cannot be deleted.'
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Banner doesn't exist."
            }
            return Response(data, status=404)
