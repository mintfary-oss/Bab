from django.urls import path
from . import api_views
app_name="pregnancy_api"
urlpatterns=[path("",api_views.PregnancyListCreateAPIView.as_view(),name="list_create"),path("<int:pk>/",api_views.PregnancyDetailAPIView.as_view(),name="detail"),path("<int:pk>/week/<int:week_num>/",api_views.WeekInfoAPIView.as_view(),name="week_info")]
