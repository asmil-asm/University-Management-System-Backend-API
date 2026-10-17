import django_filters
from django_filters import rest_framework as filters

from .models import Admission, Application, Student


class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = ['status']


class AdmissionFilter(filters.FilterSet):
    class Meta:
        model = Admission
        fields = ['program']


class ApplicationFilter(filters.FilterSet):
    apply_date_from = django_filters.DateFilter(field_name='apply_date', lookup_expr='gte')
    apply_date_to = django_filters.DateFilter(field_name='apply_date', lookup_expr='lte')

    class Meta:
        model = Application
        fields = ['student', 'program', 'status']
