from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from commonapp.serializers.rating import RatingSerializer
from commonapp.models.rating import Rating
from permission import Permission

class RatingListView(APIView):
    permission_classes = (Permission, )
    serializer_class = RatingSerializer

    # Have to modify the code.

    # def get(self, request):
    #     rating_obj = Rating.objects.all()
    #     serializers = RatingSerializer(rating_obj, many=True.\
    #         context={'request':request})
    #     data = {
    #         'success' : 1,
    #         'rating' : serializer.data,
    #     }
    #     return Response(data, status=200)

    # def post(self, request):
    #     if request.user.admin:
    #         serializer = RatingSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             data = {
    #                 'success': 1,
    #                 'rating': serializer.data
    #             }
    #             return Response(data, status=200)
    #         data = {
    #             'success': 0,
    #             'message': serializer.errors,
    #         }
    #         return Response(data, status=400)
    #     data = {
    #         'success': 0,
    #         'message': "You do not have permission to add a rating"
    #     }
    #     return Response()