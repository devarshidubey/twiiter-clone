from django.urls import path
from .views import dashboard_view, profile_list_view, profile_view, search_view, delete_view

urlpatterns = [
    path("", dashboard_view, name = "dashboard"),
    path("profile_list/", profile_list_view, name = "profile list"),
    path("profile/<username>", profile_view, name = "profile"),
    path("search/", search_view, name = "search"),
    path("delete/<pk>", delete_view, name = "delete"),
]