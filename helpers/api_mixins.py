from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status

# from permissions.permissions import GenericPermission
from rest_framework.permissions import IsAuthenticated


class FAPIMixin:
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_obsolete = True
        instance.save()
    # def get_throttles(self):
    #     # allow support for @throttle_classes decorator in view methods
    #     action_func = getattr(self, self.action)
    #     if hasattr(action_func, 'throttle_classes'):
    #         return [t() for t in getattr(action_func, 'throttle_classes')]
    #     else:
    #         return super().get_throttles()


class IntegrityExceptionCacher:
    integrity_error_message = "Integrity error."

    def create(self, request, *args, **kwargs):
        try:
            return super(
                IntegrityExceptionCacher, self).create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"detail": self.integrity_error_message}, status.HTTP_400_BAD_REQUEST)
