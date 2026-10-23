from core.dashboard_base import StaffModelViewSet

from .filters import LibraryFilter, ServiceFilter
from .models import Library, Service
from .serializers import LibrarySerializer, ServiceSerializer


class DashboardServiceViewSet(StaffModelViewSet):
    serializer_class = ServiceSerializer
    filterset_class = ServiceFilter
    search_fields = ['name_ar', 'name_en', 'description_ar', 'description_en', 'service_type']
    ordering_fields = ['id', 'name_ar', 'service_type']
    ordering = ['name_ar']

    def get_queryset(self):
        return Service.objects.all()



class DashboardLibraryViewSet(StaffModelViewSet):
    serializer_class = LibrarySerializer
    filterset_class = LibraryFilter
    search_fields = ['name_ar', 'name_en', 'location_ar', 'location_en']
    ordering_fields = ['id', 'name_ar', 'name_en']
    ordering = ['name_ar']

    def get_queryset(self):
        return Library.objects.select_related('university').all()