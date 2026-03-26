from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("password-reset/", views.UserPasswordResetView.as_view(), name="password_reset"),
    path("profile/<int:user_id>/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),
]
