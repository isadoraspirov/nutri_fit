from django.contrib import admin

from .models import WorkoutPlan

# Register your models here.

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "price")
    search_fields = ("name", "level")