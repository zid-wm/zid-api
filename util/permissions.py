from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework_api_key.models import APIKey


class HasAPIKeyOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if 'HTTP_AUTHORIZATION' in request.META:
            try:
                key = request.META['HTTP_AUTHORIZATION'].split()[1]
            except IndexError:
                return False

            try:
                api_key = APIKey.objects.get_from_key(key)
                if api_key.has_expired or not api_key.is_valid(key):
                    return False
            except ObjectDoesNotExist:
                return False
            return True

        return False
