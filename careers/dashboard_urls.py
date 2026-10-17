from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .dashboard_views import DashboardJobApplicationViewSet, DashboardJobPostingViewSet

router = DefaultRouter()
router.register(r'postings', DashboardJobPostingViewSet, basename='dashboard-job-posting')
router.register(r'applications', DashboardJobApplicationViewSet, basename='dashboard-job-application')

urlpatterns = [
    path('', include(router.urls)),
]
