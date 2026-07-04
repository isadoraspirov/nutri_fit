from django.shortcuts import render

from .models import NutritionPlan


def home(request):
    plans = NutritionPlan.objects.all()

    context = {
        "plans": plans,
    }

    return render(
        request,
        "nutrition/home.html",
        context,
    )