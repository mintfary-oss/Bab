from django.urls import path
from . import api_views
app_name="search_api"
urlpatterns=[path("",api_views.SearchAPIView.as_view(),name="search")]
