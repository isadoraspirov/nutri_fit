from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="nutrition_home"),
]