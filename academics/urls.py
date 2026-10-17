from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollegeViewSet, DepartmentViewSet, ProgramViewSet, AcademicStaffViewSet, ResearchViewSet

router = DefaultRouter()
router.register(r'colleges', CollegeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'staff', AcademicStaffViewSet)
router.register(r'research', ResearchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
