from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from nutrition.models import NutritionPlan
from .forms import OrderForm
from .models import OrderItem


def checkout(request):

    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect(reverse("nutrition_home"))

    if request.method == "POST":

        order_form = OrderForm(request.POST)

        if order_form.is_valid():

            order = order_form.save()

            for plan_id, quantity in cart.items():

                plan = NutritionPlan.objects.get(pk=plan_id)

                OrderItem.objects.create(
                    order=order,
                    nutrition_plan=plan,
                    quantity=quantity,
                    line_total=plan.price * quantity,
                )

            del request.session["cart"]

            messages.success(
                request,
                "Thank you! Your order has been placed."
            )

            return redirect("nutrition_home")

    else:

        order_form = OrderForm()

    context = {
        "order_form": order_form,
    }

    return render(
        request,
        "payments/checkout.html",
        context,
    )