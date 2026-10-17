from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters, permissions, viewsets

from .pagination import PublicPageNumberPagination
PUBLIC_READ_ONLY_FILTER_BACKENDS = [
    DjangoFilterBackend,
    drf_filters.SearchFilter,
    drf_filters.OrderingFilter,
]


class PublicReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    filter_backends = PUBLIC_READ_ONLY_FILTER_BACKENDS
    pagination_class = PublicPageNumberPagination
