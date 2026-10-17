from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, AdmissionViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'info', AdmissionViewSet)
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
