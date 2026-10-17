from core.dashboard_base import StaffModelViewSet
from rest_framework import status
from rest_framework.response import Response

from .filters import AdmissionFilter, ApplicationFilter, StudentFilter
from .models import Admission, Application, Student
from .serializers import (
    AdmissionSerializer,
    ApplicationCreateSerializer,
    ApplicationSerializer,
    StudentSerializer,
)


class DashboardStudentViewSet(StaffModelViewSet):
    serializer_class = StudentSerializer
    filterset_class = StudentFilter
    search_fields = ['full_name', 'email', 'national_id']
    ordering_fields = ['id', 'full_name', 'email', 'status']
    ordering = ['full_name']

    def get_queryset(self):
        return Student.objects.prefetch_related('applications').filter(status='accepted')


class DashboardAdmissionViewSet(StaffModelViewSet):
    serializer_class = AdmissionSerializer
    filterset_class = AdmissionFilter
    search_fields = [
        'requirements_en', 'requirements_ar', 
        'procedure_en', 'procedure_ar', 
        'academic_calendar'
    ]
    ordering_fields = ['id', 'tuition_fee']
    ordering = ['id']

    def get_queryset(self):
        return Admission.objects.select_related('program__department__college__university').all()


class DashboardApplicationViewSet(StaffModelViewSet):
    serializer_class = ApplicationSerializer
    filterset_class = ApplicationFilter
    search_fields = ['status', 'student__full_name', 'student__email', 'program__name_ar']
    ordering_fields = ['apply_date', 'id', 'status']
    ordering = ['-apply_date']

    def get_queryset(self):
        return Application.objects.select_related(
            'student',
            'program__department__college__university',
        ).all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": "تم إنشاء طلب الالتحاق بنجاح ومعالجة بيانات الطالب.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )