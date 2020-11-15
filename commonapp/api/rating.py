from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from commonapp.serializers.rating import RatingSerializer
from commonapp.models.rating import Rating
from permission import isUser

class CompanyRatingListView(generics.GenericAPIView):
    permission_classes = (isUser, )
    serializer_class = RatingSerializer

    def get(self, request, company_id):
        """
        An endpoint for listing all the vendor's ratings. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        rating_obj = Rating.objects.filter(company=company_id).order_by('-id')
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        paginator = Paginator(rating_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = RatingSerializer(page_obj, many=True,\
            context={'request':request})
        if page_obj.has_previous():
            previous_page = page_obj.previous_page_number()
        else:
            previous_page = None
        if page_obj.has_next():
            next_page = page_obj.next_page_number()
        else:
            next_page = None
        data = {
            'success': 1,
            'previous_page': previous_page,
            'next_page': next_page,
            'page_count': paginator.num_pages,
            'data': serializer.data,
        }
        return Response(data, status=200)

    def post(self, request, company_id):
        """
        An endpoint for creating vendor's rating.
        """
        serializer = RatingSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors
        }
        return Response(data, status=400)


class CompanyRatingDetailView(generics.GenericAPIView):
    permission_classes = (isUser, )
    serializer_class = RatingSerializer

    def get(self, request, company_id, rating_id):
        """
        An endpoint for getting vendor's rating detail.
        """
        rating_obj = Rating.objects.filter(id=rating_id, company=company_id)
        if rating_obj:
            serializer = RatingSerializer(rating_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data,
            }
            return Response(data, status=200)
        data = {
            'success' : 0,
            'message' : "Rating doesn't exist."
        }
        return Response(data, status=404)

    def put(self, request, company_id, rating_id):
        """
        An endpoint for updating vendor's rating detail.
        """
        rating_obj = Rating.objects.filter(id=rating_id, company=company_id)
        if rating_obj:
            serializer = RatingSerializer(instance=rating_obj[0],\
                data=request.data, partial=True, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'data': serializer.data
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "Rating doesn't exist."
        }
        return Response(data, status=404)

    def delete(self, request, company_id, rating_id):
        """
        An endpoint for deleting vendor's rating.
        """
        rating_obj = Rating.objects.filter(id=rating_id, company=company_id)
        if rating_obj:
            try:
                rating_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': 'Rating cannot be deleted.'
                }
                return Response(data, status=400)
        data = {
            'success': 0,
            'message': "Rating doesn't exist."
        }
        return Response(data, status=404)
