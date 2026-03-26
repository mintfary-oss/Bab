from django.urls import path
from . import views
app_name="media_app"
urlpatterns=[path("<int:media_id>/",views.media_detail_view,name="detail"),path("my/",views.my_media_view,name="my_media")]
