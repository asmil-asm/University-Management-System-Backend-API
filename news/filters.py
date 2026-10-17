import django_filters
from django_filters import rest_framework as filters

from .models import Announcement, Event, News


class NewsFilter(filters.FilterSet):
    publish_date_from = django_filters.DateFilter(field_name='publish_date', lookup_expr='gte')
    publish_date_to = django_filters.DateFilter(field_name='publish_date', lookup_expr='lte')

    class Meta:
        model = News
        fields = ['university']


class EventFilter(filters.FilterSet):
    event_date_from = django_filters.DateTimeFilter(field_name='event_date', lookup_expr='gte')
    event_date_to = django_filters.DateTimeFilter(field_name='event_date', lookup_expr='lte')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['university']


class AnnouncementFilter(filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Announcement
        fields = ['university']
