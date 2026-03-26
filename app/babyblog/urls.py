from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("posts/", include("posts.urls")),
    path("media/", include("media_app.urls")),
    path("pregnancy/", include("pregnancy.urls")),
    path("hospitals/", include("hospitals.urls")),
    path("chat/", include("chat.urls")),
    path("search/", include("search_app.urls")),
    path("moderation/", include("admin_panel.urls")),
    path("api/", include("babyblog.api_urls")),
    path("", include("posts.urls_feed")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
