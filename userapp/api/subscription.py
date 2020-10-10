from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from userapp.models.user import User
from userapp.models.subscription import Subscription
from userapp.serializers.subscription import SubscriptionSerializer

# Implement api for creating, editing, deleting subscription

class CreateSubscription(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SubscriptionSerializer

    def post(self, request):
        """
        An endpoint for subscription registration.
        """
        if not Subscription.objects.filter(email=request.cleaned_data['email']):
            serializer = SubscriptionSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'subscription': 'You have been subscribed.'
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': serializers.error
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': 'User already subscribed.'
            }
            return Response(data, status=409)

class UpdateSubscription(generics.GenericAPIView):
    serializer_class = SubscriptionSerializer

    def get(self, request, subscription_id):
        """
        An endpoint for getting subscription detail.
        """
        if Subscription.objects.filter(id=subscription_id):
            subscription_obj = Subscription.objects.get(id=subscription_id)
            serializer = SubscriptionSerializer(subscription_obj,\
                context={'request': request})
            data = {
                'success': 1,
                'subscription': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': "Subscription doesn't exist."
        }
        return Response(data, status=404)
    
    def put(self, request, subscription_id):
        """
        An endpoint for updating subscription detail.
        """
        if Subscription.objects.filter(id=subscription_id):
            subscription_obj = Subscription.objects.get(id=subscription_id)
            serializer = SubscriptionSerializer(instance=subscription_obj,\
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'subscription': serializer.data
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "Subscription doesn't exist."
        }
        return Response(data, status=404)
    
    def delete(self, request, subscription_id):
        """
        An endpoint for deleting subscription.
        """
        if Subscription.objects.filter(id=subscription_id):
            subscription_obj = Subscription.objects.get(id=subscription_id)
            subscription_obj.delete()
            data = {
                'success': 1,
                'subscription': 'Subscription deleted successfully.'
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': "Subscription doesn't exist."
        }
        return Response(data, status=404)