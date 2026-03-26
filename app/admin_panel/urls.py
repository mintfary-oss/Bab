from django.urls import path
from . import views
app_name="admin_panel"
urlpatterns=[path("",views.moderation_dashboard_view,name="dashboard"),path("report/<int:report_id>/",views.report_detail_view,name="report_detail"),path("backup/create/",views.backup_create_view,name="backup_create"),path("backup/download/<str:filename>/",views.backup_download_view,name="backup_download")]
