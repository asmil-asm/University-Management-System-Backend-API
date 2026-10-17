from core.dashboard_base import StaffModelViewSet

from .filters import JobApplicationFilter, JobPostingFilter
from .models import JobApplication, JobPosting
from .serializers import JobApplicationSerializer, JobPostingSerializer


class DashboardJobPostingViewSet(StaffModelViewSet):
    serializer_class = JobPostingSerializer
    filterset_class = JobPostingFilter
    search_fields = [
        'title_en', 'title_ar', 
        'description_en', 'description_ar', 
        'requirements_en', 'requirements_ar', 
        'job_type'
    ]
    ordering_fields = ['deadline', 'id', 'title_en', 'title_ar', 'status']
    ordering = ['-deadline']

    def get_queryset(self):
        return JobPosting.objects.select_related('university').all()


class DashboardJobApplicationViewSet(StaffModelViewSet):
    serializer_class = JobApplicationSerializer
    filterset_class = JobApplicationFilter
    search_fields = ['applicant_name', 'applicant_email']
    ordering_fields = ['apply_date', 'id', 'status']
    ordering = ['-apply_date']

    def get_queryset(self):
        return JobApplication.objects.select_related('job__university').all()