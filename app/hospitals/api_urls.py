from django.urls import path
from . import api_views
app_name="hospitals_api"
urlpatterns=[path("",api_views.HospitalListAPIView.as_view(),name="list"),path("<int:pk>/",api_views.HospitalDetailAPIView.as_view(),name="detail"),path("<int:hospital_id>/reviews/",api_views.HospitalReviewListCreateAPIView.as_view(),name="reviews")]
