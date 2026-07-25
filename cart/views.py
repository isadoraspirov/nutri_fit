from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

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


@require_POST
def update_cart(request, item_key):
    """
    Update the quantity of an item in the cart.
    """
    cart = request.session.get("cart", {})

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if item_key not in cart:
        messages.error(request, "That item is not in your cart.")
        return redirect("cart:view_cart")

    if quantity > 0:
        cart[item_key] = quantity
        messages.success(request, "Cart quantity updated.")
    else:
        cart.pop(item_key, None)
        messages.success(request, "Item removed from your cart.")

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart:view_cart")


@require_POST
def remove_from_cart(request, item_key):
    """
    Remove an item completely from the cart.
    """
    cart = request.session.get("cart", {})

    if item_key in cart:
        cart.pop(item_key)
        messages.success(request, "Item removed from your cart.")
    else:
        messages.error(request, "That item is not in your cart.")

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart:view_cart")