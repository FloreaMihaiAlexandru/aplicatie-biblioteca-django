from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("search/", views.search_view, name="search"),
    path("rent/<int:book_id>/", views.rentBook_view, name="rentBook"),
]