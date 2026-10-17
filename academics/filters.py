import django_filters
from django_filters import rest_framework as filters

from .models import AcademicStaff, College, Department, Program, Research


class CollegeFilter(filters.FilterSet):
    class Meta:
        model = College
        fields = ['university']


class DepartmentFilter(filters.FilterSet):
    class Meta:
        model = Department
        fields = ['college']


class ProgramFilter(filters.FilterSet):
    class Meta:
        model = Program
        fields = ['department', 'level']


class AcademicStaffFilter(filters.FilterSet):
    class Meta:
        model = AcademicStaff
        fields = ['department', 'staff_type']


class ResearchFilter(filters.FilterSet):
    published_from = django_filters.DateFilter(field_name='published_date', lookup_expr='gte')
    published_to = django_filters.DateFilter(field_name='published_date', lookup_expr='lte')

    class Meta:
        model = Research
        fields = ['staff']
