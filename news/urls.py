from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, EventViewSet, AnnouncementViewSet

router = DefaultRouter()
router.register(r'articles', NewsViewSet)
router.register(r'events', EventViewSet)
router.register(r'announcements', AnnouncementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
