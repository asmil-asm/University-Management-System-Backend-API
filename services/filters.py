from django_filters import rest_framework as filters

from .models import Library, Service


class ServiceFilter(filters.FilterSet):
    class Meta:
        model = Service
        fields = ['service_type']


class LibraryFilter(filters.FilterSet):
    class Meta:
        model = Library
        fields = ['university']
