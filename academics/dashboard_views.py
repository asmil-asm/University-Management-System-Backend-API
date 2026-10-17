from core.dashboard_base import StaffModelViewSet

from .filters import (
    AcademicStaffFilter,
    CollegeFilter,
    DepartmentFilter,
    ProgramFilter,
    ResearchFilter,
)
from .models import AcademicStaff, College, Department, Program, Research
from .serializers import (
    AcademicStaffSerializer,
    CollegeSerializer,
    DepartmentSerializer,
    ProgramSerializer,
    ResearchSerializer,
)


class DashboardCollegeViewSet(StaffModelViewSet):
    serializer_class = CollegeSerializer
    filterset_class = CollegeFilter
    search_fields = ['name_ar', 'name_en', 'description_ar', 'description_en']
    ordering_fields = ['id', 'name_ar', 'name_en']
    ordering = ['name_ar']

    def get_queryset(self):
        return College.objects.select_related('university').prefetch_related(
            'images',
            'departments__programs',
            'departments__staff',
        ).all()


class DashboardDepartmentViewSet(StaffModelViewSet):
    serializer_class = DepartmentSerializer
    filterset_class = DepartmentFilter
    search_fields = ['name_ar', 'name_en']
    ordering_fields = ['id', 'name_ar', 'name_en']
    ordering = ['name_ar']

    def get_queryset(self):
        return Department.objects.select_related('college__university').prefetch_related(
            'programs',
            'staff',
        ).all()


class DashboardProgramViewSet(StaffModelViewSet):
    serializer_class = ProgramSerializer
    filterset_class = ProgramFilter
    search_fields = ['name_ar', 'name_en', 'level']
    ordering_fields = ['id', 'name_ar', 'name_en', 'level']
    ordering = ['name_ar']

    def get_queryset(self):
        return Program.objects.select_related('department__college__university').all()


class DashboardAcademicStaffViewSet(StaffModelViewSet):
    serializer_class = AcademicStaffSerializer
    filterset_class = AcademicStaffFilter
    search_fields = ['full_name', 'title_en', 'title_ar', 'email', 'bio_ar', 'bio_en', 'staff_type']
    ordering_fields = ['id', 'full_name', 'staff_type']
    ordering = ['full_name']

    def get_queryset(self):
        return AcademicStaff.objects.select_related('department__college__university').prefetch_related(
            'researches',
        ).all()


class DashboardResearchViewSet(StaffModelViewSet):
    serializer_class = ResearchSerializer
    filterset_class = ResearchFilter
    search_fields = ['title_ar', 'title_en', 'abstract_ar', 'abstract_en']
    ordering_fields = ['published_date', 'id', 'title_ar', 'title_en']
    ordering = ['-published_date']

    def get_queryset(self):
        return Research.objects.select_related('staff__department__college__university').all()