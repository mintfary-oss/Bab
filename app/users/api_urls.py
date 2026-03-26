from django.urls import path
from . import api_views
app_name="users_api"
urlpatterns=[path("register/",api_views.RegisterAPIView.as_view(),name="register"),path("me/",api_views.CurrentUserAPIView.as_view(),name="me"),path("<int:pk>/",api_views.UserDetailAPIView.as_view(),name="detail"),path("<int:pk>/profile/",api_views.ProfileUpdateAPIView.as_view(),name="profile_update")]
