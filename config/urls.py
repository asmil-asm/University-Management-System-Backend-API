from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/core/', include('core.urls')),
    path('api/v1/academics/', include('academics.urls')),
    path('api/v1/news/', include('news.urls')),
    path('api/v1/dashboard/', include('config.dashboard_urls')),
    path('api/v1/careers/', include('careers.urls')),
    path('api/v1/admissions/', include('admissions.urls')),
    path('api/v1/services/', include('services.urls')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]