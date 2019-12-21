from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="vuln-dash"),
    path("vuln/list/", views.VulnListView.as_view(), name="vuln-list"),
    path("vuln/list/reversed/", views.ReversedVulnListView.as_view(), name="vuln-list-rev"),
    path("vuln/list/ranked/", views.RankedVulnListView.as_view(), name="vuln-list-rank"),
    path("vuln/<int:pk>/", views.VulnDetailView.as_view(), name="vuln-detail"),
    path("vuln/new/", views.VulnCreateView.as_view(), name="vuln-create"),
    path("vuln/<int:pk>/update/", views.VulnUpdateView.as_view(), name="vuln-update"),
    path("vuln/<int:pk>/delete/", views.VulnDeleteView.as_view(), name="vuln-delete"),
    path("rem/list/", views.RemedyListView.as_view(), name="rem-list"),
    path('rem/<int:pk>/new/', views.add_remedy, name='add-remedy'),
    path("vuln/<int:pk>/export/", views.export_csv, name="export-csv"),
    path("vuln/search/", views.VulnSearchListView.as_view(), name="vuln-search"),
    path("rem/search/", views.RemedySearchListView.as_view(), name="rem-search")
]
