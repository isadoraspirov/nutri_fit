from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse

from nutrition.models import NutritionPlan
from .forms import OrderForm
from .models import Order, OrderItem


def checkout(request):
    """
    Display the checkout page and create an order.
    """

    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect(reverse("nutrition_home"))

    if request.method == "POST":

        order_form = OrderForm(request.POST)

        if order_form.is_valid():

            order = order_form.save()

            # Create one OrderItem for each plan in the cart
            for plan_id, quantity in cart.items():

                plan = NutritionPlan.objects.get(pk=plan_id)

                OrderItem.objects.create(
                    order=order,
                    nutrition_plan=plan,
                    quantity=quantity,
                    line_total=plan.price * quantity,
                )

            # Calculate the order total
            order.order_total = sum(
                item.line_total for item in order.items.all()
            )

            order.save()

            # Empty the cart
            del request.session["cart"]

            messages.success(
                request,
                "Thank you for your purchase!"
            )

            return redirect(
                "payments:checkout_success",
                order_number=order.order_number,
            )

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


def checkout_success(request, order_number):
    """
    Display a successful order.
    """

    order = get_object_or_404(
        Order,
        order_number=order_number,
    )

    messages.success(
        request,
        "Your nutrition plan has been purchased successfully!"
    )

    context = {
        "order": order,
    }

    return render(
        request,
        "payments/checkout_success.html",
        context,
    )