from .dashboard_base import StaffModelViewSet
from .filters import (
    BranchFilter,
    ContactMessageFilter,
    LanguageFilter,
    PageFilter,
    SocialMediaFilter,
    UniversityFilter,
)
from .models import Branch, ContactMessage, Language, Page, SocialMedia, University
from .serializers import (
    BranchSerializer,
    ContactMessageSerializer,
    LanguageSerializer,
    PageSerializer,
    SocialMediaSerializer,
    UniversitySerializer,
)


class DashboardUniversityViewSet(StaffModelViewSet):
    serializer_class = UniversitySerializer
    filterset_class = UniversityFilter
    search_fields = ['name_ar', 'name_en', 'location', 'email', 'phone']
    ordering_fields = ['id', 'name_ar', 'name_en']
    ordering = ['id']

    def get_queryset(self):
        return University.objects.prefetch_related('social_links', 'branches').all()


class DashboardLanguageViewSet(StaffModelViewSet):
    serializer_class = LanguageSerializer
    filterset_class = LanguageFilter
    search_fields = ['code', 'label']
    ordering_fields = ['code', 'label', 'id']
    ordering = ['code']

    def get_queryset(self):
        return Language.objects.all()


class DashboardSocialMediaViewSet(StaffModelViewSet):
    serializer_class = SocialMediaSerializer
    filterset_class = SocialMediaFilter
    search_fields = ['platform', 'url']
    ordering_fields = ['id', 'platform']
    ordering = ['id']

    def get_queryset(self):
        return SocialMedia.objects.select_related('university').all()


class DashboardBranchViewSet(StaffModelViewSet):
    serializer_class = BranchSerializer
    filterset_class = BranchFilter
    search_fields = ['name', 'address']
    ordering_fields = ['id', 'name']
    ordering = ['name']

    def get_queryset(self):
        return Branch.objects.select_related('university').all()


class DashboardPageViewSet(StaffModelViewSet):
    serializer_class = PageSerializer
    filterset_class = PageFilter
    search_fields = ['slug', 'title_ar', 'title_en', 'content_ar', 'content_en']
    ordering_fields = ['slug', 'title_ar', 'page_type', 'id']
    ordering = ['slug']

    def get_queryset(self):
        return Page.objects.all()


class DashboardContactMessageViewSet(StaffModelViewSet):
    serializer_class = ContactMessageSerializer
    filterset_class = ContactMessageFilter
    search_fields = [
        'sender_name',
        'sender_email',
        'subject_ar',
        'subject_en',
        'message_ar',
        'message_en',
    ]
    ordering_fields = ['sent_at', 'status', 'id']
    ordering = ['-sent_at']

    def get_queryset(self):
        return ContactMessage.objects.all()
