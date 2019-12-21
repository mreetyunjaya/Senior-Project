from django.urls import path
from . import views

urlpatterns = [
    path("welcome/", views.welcome, name="webroot-welcome"),
    path("about/", views.about, name="webroot-about")
]
