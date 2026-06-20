from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout, name="payments_checkout"),
]