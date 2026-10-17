from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .dashboard_views import (
    DashboardAdmissionViewSet,
    DashboardApplicationViewSet,
    DashboardStudentViewSet,
)

router = DefaultRouter()
router.register(r'students', DashboardStudentViewSet, basename='dashboard-student')
router.register(r'info', DashboardAdmissionViewSet, basename='dashboard-admission-info')
router.register(r'applications', DashboardApplicationViewSet, basename='dashboard-application')

urlpatterns = [
    path('', include(router.urls)),
]
