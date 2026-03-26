from django.urls import path
from . import views
app_name="hospitals"
urlpatterns=[path("",views.hospital_list_view,name="list"),path("<int:hospital_id>/",views.hospital_detail_view,name="detail"),path("<int:hospital_id>/review/",views.hospital_review_view,name="review")]
