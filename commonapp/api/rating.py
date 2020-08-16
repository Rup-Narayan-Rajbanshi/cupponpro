from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from commonapp.serializers.rating import RatingSerializer
from commonapp.models.rating import Rating
from permission import Permission

class CompanyRatingListView(APIView):
    permission_classes = (Permission, )
    serializer_class = RatingSerializer

    def get(self, request, company_id):
        rating_obj = Rating.objects.filter(company=company_id)
        if rating_obj:
            serializer = RatingSerializer(rating_obj, many=True)
            data = {
                'success' : 1,
                'rating' : serializer.data,
            }
            return Response(data, status=200)
        data = {
            'success' : 0,
            'message' : 'No rating found.',
        }
        return Response(data, status=400)

    def post(self, request, company_id):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'rating': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors,
        }
        return Response(data, status=400)

class CompanyRatingDetailView(APIView):
    permission_classes = (Permission, )
    serializer_class = RatingSerializer

    def get(self, request, company_id, rating_id):
        if Rating.objects.filter(id=rating_id, company=company_id):
            rating_obj = Rating.objects.get(id=rating_id)
            serializer = RatingSerializer(rating_obj)
            data = {
                'success' : 1,
                'rating' : serializer.data,
            }
            return Response(data, status=200)
        data = {
            'success' : 0,
            'message' : 'Rating id not found.',
        }
        return Response(data, status=400)


    def put(self, request, company_id, rating_id):
        if Rating.objects.filter(id=rating_id, company=company_id):
            rating_obj = Rating.objects.get(id=rating_id)
            serializer = RatingSerializer(instance=rating_obj,\
                data=request.data, partial=True)
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
            'message': "Rating id not found."
        }
        return Response(data, status=400)

    def delete(self, request, company_id, rating_id):
        if Rating.objects.filter(id=rating_id, company=company_id):
            rating_obj = Rating.objects.get(id=rating_id)
            rating_obj.delete()
            data = {
                'success': 1,
                'rating': "Rating deleted successfully."
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': "Rating id not found."
        }
        return Response(data, status=400)