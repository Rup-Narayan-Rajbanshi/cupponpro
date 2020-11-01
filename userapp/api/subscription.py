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
        if not Subscription.objects.filter(email=request.data['email']):
            serializer = SubscriptionSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user_obj = User.objects.filter(email=request.data['email'])
                if user_obj:
                    serializer.save(user=user_obj[0], email=request.data['email'], promotion=request.data['promotion'])
                else:
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
                'message': 'User already subscribed.'
            }
            return Response(data, status=400)

class UpdateSubscription(generics.GenericAPIView):
    serializer_class = SubscriptionSerializer

    def get(self, request, subscription_id):
        """
        An endpoint for getting subscription detail.
        """
        subscription_obj = Subscription.objects.filter(id=subscription_id)
        if subscription_obj:
            serializer = SubscriptionSerializer(subscription_obj[0],\
                context={'request': request})
            data = {
                'success': 1,
                'data': serializer.data
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
        subscription_obj = Subscription.objects.filter(id=subscription_id)
        if subscription_obj:
            serializer = SubscriptionSerializer(instance=subscription_obj[0],\
                data=request.data, context={'request': request})
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
            'message': "Subscription doesn't exist."
        }
        return Response(data, status=404)
    
    def delete(self, request, subscription_id):
        """
        An endpoint for deleting subscription.
        """
        subscription_obj = Subscription.objects.filter(id=subscription_id)
        if subscription_obj:
            try:
                subscription_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': 'Subscription cannot be deleted.'
                }
                return Response(data, status=400)
        data = {
            'success': 0,
            'message': "Subscription doesn't exist."
        }
        return Response(data, status=404)