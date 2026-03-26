from django.urls import path

from . import views

app_name = "pregnancy"
urlpatterns = [
    path("", views.pregnancy_dashboard_view, name="dashboard"),
    path("create/", views.pregnancy_create_view, name="create"),
    path("weeks/", views.weeks_overview_view, name="weeks_overview"),
    path("week/<int:week_num>/", views.week_detail_view, name="week_detail"),
    path("checklist/<int:item_id>/toggle/", views.checklist_toggle_view, name="checklist_toggle"),
]
