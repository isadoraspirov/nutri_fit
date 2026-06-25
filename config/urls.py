from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include("allauth.urls")),
    path("", include("home.urls")),

    path("nutrition/", include("nutrition.urls")),
    path("workouts/", include("workouts.urls")),
    path("payments/", include("payments.urls")),
]

