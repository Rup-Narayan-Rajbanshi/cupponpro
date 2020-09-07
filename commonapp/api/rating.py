from rest_framework.views import APIView
from rest_framework.response import Response
from commonapp.serializers.rating import RatingSerializer
from commonapp.models.rating import Rating
from permission import isUser

class CompanyRatingListView(APIView):
    permission_classes = (isUser, )
    serializer_class = RatingSerializer

    def get(self, request, company_id):
        rating_obj = Rating.objects.filter(company=company_id).order_by('-id')
        if rating_obj:
            serializer = RatingSerializer(rating_obj, many=True,\
                context={'request':request})
            data = {
                'success' : 1,
                'rating' : serializer.data,
            }
            return Response(data, status=200)
        data = {
            'success' : 0,
            'message' : "Rating doesn't exist.",
        }
        return Response(data, status=400)

    def post(self, request, company_id):
        if int(request.data['company']) == company_id:
            serializer = RatingSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'rating': serializer.data
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Rating failed."
            }
            return Response(data, status=400)

class CompanyRatingDetailView(APIView):
    permission_classes = (isUser, )
    serializer_class = RatingSerializer

    def get(self, request, company_id, rating_id):
        rating_obj = Rating.objects.filter(id=rating_id, company=company_id)
        if rating_obj:
            serializer = RatingSerializer(rating_obj[0], context={'request':request})
            data = {
                'success' : 1,
                'rating' : serializer.data,
            }
            return Response(data, status=200)
        data = {
            'success' : 0,
            'message' : "Rating doesn't exist."
        }
        return Response(data, status=404)

    def put(self, request, company_id, rating_id):
        if int(request.data['company']) == company_id:
            rating_obj = Rating.objects.filter(id=rating_id, company=company_id)
            if rating_obj:
                serializer = RatingSerializer(instance=rating_obj[0],\
                    data=request.data, partial=True, context={'request':request})
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success': 1,
                        'rating': serializer.data
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
        else:
            data = {
                'success': 0,
                'message': "Rating Failed."
            }
            return Response(data, status=400)

    def delete(self, request, company_id, rating_id):
        rating_obj = Rating.objects.filter(id=rating_id, company=company_id)
        if rating_obj:
            try:
                rating_obj[0].delete()
                data = {
                    'success': 1,
                    'rating': "Rating deleted successfully."
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
