
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('captured/', include('captured_moments.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/events/', include('events.urls')),
    path('api/groups/', include('groups.urls')),
    path('news/', include('news.urls')),
    path('api/calendar/', include('readings.urls')),
    path('api/blogs/', include('blogs.urls')),
    path('api/theme/', include('theme.urls')),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)