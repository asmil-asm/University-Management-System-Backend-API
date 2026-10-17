import django_filters
from django_filters import rest_framework as filters

from .models import JobApplication, JobPosting


class JobPostingFilter(filters.FilterSet):
    deadline_from = django_filters.DateFilter(field_name='deadline', lookup_expr='gte')
    deadline_to = django_filters.DateFilter(field_name='deadline', lookup_expr='lte')

    class Meta:
        model = JobPosting
        fields = ['university', 'status', 'job_type']


class JobApplicationFilter(filters.FilterSet):
    apply_date_from = django_filters.DateFilter(field_name='apply_date', lookup_expr='gte')
    apply_date_to = django_filters.DateFilter(field_name='apply_date', lookup_expr='lte')

    class Meta:
        model = JobApplication
        fields = ['job', 'status']
