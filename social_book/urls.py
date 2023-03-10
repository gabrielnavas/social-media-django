from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('feed.urls')),
    path('', include('settings.urls')),
]

# config from upload image
urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT,
) 