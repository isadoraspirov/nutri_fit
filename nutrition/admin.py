from django.contrib import admin
from .models import NutritionPlan


@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "duration_weeks",
    )