from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from nutrition.models import NutritionPlan


def add_to_cart(request, plan_id):
    """
    Add a nutrition plan to the shopping cart.
    """

    plan = get_object_or_404(NutritionPlan, pk=plan_id)

    cart = request.session.get("cart", {})

    plan_id = str(plan_id)

    if plan_id in cart:
        cart[plan_id] += 1
    else:
        cart[plan_id] = 1

    request.session["cart"] = cart

    messages.success(
        request,
        f"{plan.name} has been added to your cart."
    )

    return redirect("view_cart")


def view_cart(request):
    return render(request, "cart/cart.html")