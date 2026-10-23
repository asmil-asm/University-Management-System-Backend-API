from rest_framework import viewsets, permissions
from .models import Service, Library
from .serializers import ServiceSerializer, LibrarySerializer

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class LibraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Library.objects.select_related('university').all()
    serializer_class = LibrarySerializer