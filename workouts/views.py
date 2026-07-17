from django.shortcuts import render

from .models import WorkoutPlan


def dashboard(request):
    workout_plans = WorkoutPlan.objects.all()

    context = {
        "workout_plans": workout_plans,
    }

    return render(request, "workouts/dashboard.html", context)