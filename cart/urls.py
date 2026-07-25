from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path(
        "",
        views.view_cart,
        name="view_cart",
    ),
    path(
        "add/<int:plan_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "add-workout/<int:plan_id>/",
        views.add_workout_to_cart,
        name="add_workout_to_cart",
    ),
    path(
        "update/<str:item_key>/",
        views.update_cart,
        name="update_cart",
    ),
    path(
        "remove/<str:item_key>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
]