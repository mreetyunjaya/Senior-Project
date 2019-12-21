from users import views as user_views
from django.urls import path

urlpatterns = [
    path("<str:username>/vulns", user_views.UserVulnListView.as_view(), name="user-vulns"),
    path("<str:username>/remediations", user_views.UserRemedyListView.as_view(), name="user-rems")
]
