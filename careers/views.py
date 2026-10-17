from rest_framework import viewsets, permissions
from .models import JobPosting, JobApplication
from .serializers import JobPostingSerializer, JobApplicationSerializer

class JobPostingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobPosting.objects.all().order_by('-deadline')
    serializer_class = JobPostingSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]