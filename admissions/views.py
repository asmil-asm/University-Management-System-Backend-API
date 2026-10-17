from rest_framework import permissions, viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from core.api_mixins import PublicReadOnlyViewSet
from core.pagination import PublicPageNumberPagination

from .models import Admission, Application, Student
from .serializers import (
    AdmissionSerializer,
    ApplicationCreateSerializer,
    ApplicationSerializer,
    StudentSerializer,
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('full_name')
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PublicPageNumberPagination


class AdmissionViewSet(PublicReadOnlyViewSet):
    queryset = Admission.objects.select_related('program').all()
    serializer_class = AdmissionSerializer
    permission_classes = [permissions.AllowAny]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related('student', 'program').all()
    pagination_class = PublicPageNumberPagination
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == "create":
            return ApplicationCreateSerializer
        return ApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": "Application created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )