from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from rest_framework import permissions
from rest_framework import viewsets

from .pagination import DashboardPageNumberPagination


class StaffModelViewSet(viewsets.ModelViewSet):
    """
    Base for /api/v1/dashboard/* resources: staff (is_staff) + JWT.
    List: pagination (page, page_size), django-filter, search, ordering.
    """

    permission_classes = [permissions.IsAdminUser]
    pagination_class = DashboardPageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
