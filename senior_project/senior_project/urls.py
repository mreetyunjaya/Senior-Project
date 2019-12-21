from django.contrib.auth import views as auth_views
from users import views as user_views
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("", include("vulns.urls")),
    path("user/", include("users.urls")),
    path("home/", include("webroot.urls")),
    path("register/", user_views.register, name="register"),
    path("profile/", user_views.profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('admin/', admin.site.urls)
]
