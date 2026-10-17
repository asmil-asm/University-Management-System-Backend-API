from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from rest_framework import permissions, viewsets

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


class CollegeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = College.objects.select_related('university').prefetch_related(
        'images',
        'departments__programs',
        'departments__staff',
    ).all().order_by('name_ar')
    serializer_class = CollegeSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_class = CollegeFilter
    search_fields = ['name_ar', 'name_en', 'description_ar', 'description_en']
    ordering_fields = ['id', 'name_ar', 'name_en']
    ordering = ['name_ar']


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.select_related('college__university').prefetch_related(
        'programs',
        'staff',
    ).all().order_by('name_ar')
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_class = DepartmentFilter
    search_fields = ['name_ar', 'name_en']
    ordering_fields = ['id', 'name_ar', 'name_en']
    ordering = ['name_ar']


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Program.objects.select_related('department__college__university').all().order_by('name_ar')
    serializer_class = ProgramSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_class = ProgramFilter
    search_fields = ['name_ar', 'name_en', 'level']
    ordering_fields = ['id', 'name_ar', 'name_en', 'level']
    ordering = ['name_ar']


class AcademicStaffViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AcademicStaff.objects.select_related('department__college__university').prefetch_related(
        'researches',
    ).all().order_by('full_name')
    serializer_class = AcademicStaffSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_class = AcademicStaffFilter
    search_fields = ['full_name', 'title_en', 'title_ar', 'email', 'bio_ar', 'bio_en', 'staff_type']
    ordering_fields = ['id', 'full_name', 'staff_type']
    ordering = ['full_name']


class ResearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Research.objects.select_related('staff__department__college__university').all().order_by('-published_date')
    serializer_class = ResearchSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_class = ResearchFilter
    search_fields = ['title_ar', 'title_en', 'abstract_ar', 'abstract_en']
    ordering_fields = ['published_date', 'id', 'title_ar', 'title_en']
    ordering = ['-published_date']