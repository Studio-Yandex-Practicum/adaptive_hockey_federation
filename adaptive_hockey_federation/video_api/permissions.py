from django.conf import settings
from rest_framework.permissions import BasePermission


class HasAPIDocsKey(BasePermission):
    """
    Кастомный пермишен для API ключа.
    """
    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-KEY')
        return api_key == settings.API_DOCS_KEY
