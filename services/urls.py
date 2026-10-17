from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, LibraryViewSet

router = DefaultRouter()
router.register(r'list', ServiceViewSet)
router.register(r'library', LibraryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
