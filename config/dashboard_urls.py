"""Aggregate dashboard API under /api/v1/dashboard/."""

from django.urls import include, path

urlpatterns = [
    path('core/', include('core.dashboard_urls')),
    path('academics/', include('academics.dashboard_urls')),
    path('news/', include('news.dashboard_urls')),
    path('careers/', include('careers.dashboard_urls')),
    path('admissions/', include('admissions.dashboard_urls')),
    path('services/', include('services.dashboard_urls')),
]
