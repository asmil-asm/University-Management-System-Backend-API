import django_filters
from django_filters import rest_framework as filters

from .models import Branch, ContactMessage, Language, Page, SocialMedia, University


class UniversityFilter(filters.FilterSet):
    class Meta:
        model = University
        fields = ['id']


class LanguageFilter(filters.FilterSet):
    class Meta:
        model = Language
        fields = ['code']


class SocialMediaFilter(filters.FilterSet):
    class Meta:
        model = SocialMedia
        fields = ['university', 'platform']


class BranchFilter(filters.FilterSet):
    class Meta:
        model = Branch
        fields = ['university']


class PageFilter(filters.FilterSet):
    class Meta:
        model = Page
        fields = ['page_type', 'slug']


class ContactMessageFilter(filters.FilterSet):
    sent_at_from = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_at_to = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = ContactMessage
        fields = ['status']
