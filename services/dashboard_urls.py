from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .dashboard_views import DashboardLibraryViewSet, DashboardServiceViewSet

router = DefaultRouter()
router.register(r'list', DashboardServiceViewSet, basename='dashboard-service')
router.register(r'library', DashboardLibraryViewSet, basename='dashboard-library')

urlpatterns = [
    path('', include(router.urls)),
]
