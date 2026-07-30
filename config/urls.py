from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),

    # Django-allauth
    path("accounts/", include("allauth.urls")),

    # Custom wellness profile
    path("profile/", include("accounts.urls")),

    path("nutrition/", include("nutrition.urls")),
    path("workouts/", include("workouts.urls")),
    path("cart/", include("cart.urls")),
    path("payments/", include("payments.urls")),
]