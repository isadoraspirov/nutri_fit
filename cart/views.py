from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from nutrition.models import NutritionPlan
from workouts.models import WorkoutPlan


def add_to_cart(request, plan_id):
    """
    Add a nutrition plan to the shopping cart.
    """
    plan = get_object_or_404(NutritionPlan, pk=plan_id)

    cart = request.session.get("cart", {})
    item_id = f"nutrition_{plan_id}"

    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(
        request,
        f"{plan.name} has been added to your cart.",
    )

    return redirect("cart:view_cart")


def add_workout_to_cart(request, plan_id):
    """
    Add a workout plan to the shopping cart.
    """
    plan = get_object_or_404(WorkoutPlan, pk=plan_id)

    cart = request.session.get("cart", {})
    item_id = f"workout_{plan_id}"

    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(
        request,
        f"{plan.name} has been added to your cart.",
    )

    return redirect("cart:view_cart")


def view_cart(request):
    """
    Display the shopping cart.
    """
    return render(request, "cart/cart.html")