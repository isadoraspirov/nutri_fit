from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("nutrition/", include("nutrition.urls")),
    path("workouts/", include("workouts.urls")),
    path("payments/", include("payments.urls")),
    path("", include("home.urls")),
]
