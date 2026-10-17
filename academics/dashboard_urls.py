from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .dashboard_views import (
    DashboardAcademicStaffViewSet,
    DashboardCollegeViewSet,
    DashboardDepartmentViewSet,
    DashboardProgramViewSet,
    DashboardResearchViewSet,
)

router = DefaultRouter()
router.register(r'colleges', DashboardCollegeViewSet, basename='dashboard-college')
router.register(r'departments', DashboardDepartmentViewSet, basename='dashboard-department')
router.register(r'programs', DashboardProgramViewSet, basename='dashboard-program')
router.register(r'staff', DashboardAcademicStaffViewSet, basename='dashboard-staff')
router.register(r'research', DashboardResearchViewSet, basename='dashboard-research')

urlpatterns = [
    path('', include(router.urls)),
]
