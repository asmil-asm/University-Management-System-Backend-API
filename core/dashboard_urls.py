from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .dashboard_views import (
    DashboardBranchViewSet,
    DashboardContactMessageViewSet,
    DashboardLanguageViewSet,
    DashboardPageViewSet,
    DashboardSocialMediaViewSet,
    DashboardUniversityViewSet,
)

router = DefaultRouter()
router.register(r'universities', DashboardUniversityViewSet, basename='dashboard-university')
router.register(r'languages', DashboardLanguageViewSet, basename='dashboard-language')
router.register(r'social-media', DashboardSocialMediaViewSet, basename='dashboard-social')
router.register(r'branches', DashboardBranchViewSet, basename='dashboard-branch')
router.register(r'pages', DashboardPageViewSet, basename='dashboard-page')
router.register(r'contact-messages', DashboardContactMessageViewSet, basename='dashboard-contact')

urlpatterns = [
    path('', include(router.urls)),
]
