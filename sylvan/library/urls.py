from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("status/", views.status_list, name="status"),
]