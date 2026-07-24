from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("accounts/", include("allauth.urls")),
    path("nutrition/", include("nutrition.urls")),
    path("workouts/", include("workouts.urls")),
    path("payments/", include("payments.urls")),
    path("cart/", include("cart.urls")),
]