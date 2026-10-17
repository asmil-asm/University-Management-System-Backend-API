from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .dashboard_views import (
    DashboardAnnouncementViewSet,
    DashboardEventViewSet,
    DashboardNewsViewSet,
)

router = DefaultRouter()
router.register(r'articles', DashboardNewsViewSet, basename='dashboard-news')
router.register(r'events', DashboardEventViewSet, basename='dashboard-event')
router.register(r'announcements', DashboardAnnouncementViewSet, basename='dashboard-announcement')

urlpatterns = [
    path('', include(router.urls)),
]
