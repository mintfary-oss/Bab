from django.urls import path

from posts import views

urlpatterns = [path("", views.feed_view, name="home")]
