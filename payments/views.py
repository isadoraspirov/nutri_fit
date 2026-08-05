from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse

from accounts.models import CustomerProfile
from nutrition.models import NutritionPlan
from workouts.models import WorkoutPlan

from .forms import OrderForm
from .models import Order, OrderItem


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """
    Display the checkout form, create an order and redirect
    the customer to Stripe Checkout.
    """
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(
            request,
            "Your cart is empty.",
        )
        return redirect("nutrition_home")

    if request.method == "POST":
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            try:
                with transaction.atomic():
                    order = order_form.save(commit=False)
                    order.user = request.user
                    order.save()

                    for item_key, quantity in cart.items():
                        try:
                            item_type, plan_id = item_key.split(
                                "_",
                                1,
                            )
                            plan_id = int(plan_id)
                            quantity = int(quantity)

                        except (ValueError, TypeError):
                            raise ValueError(
                                f"Invalid cart item: {item_key}"
                            )

                        if quantity < 1:
                            raise ValueError(
                                f"Invalid quantity for: {item_key}"
                            )

                        if item_type == "nutrition":
                            plan = get_object_or_404(
                                NutritionPlan,
                                pk=plan_id,
                            )

                            OrderItem.objects.create(
                                order=order,
                                nutrition_plan=plan,
                                quantity=quantity,
                            )

                        elif item_type == "workout":
                            plan = get_object_or_404(
                                WorkoutPlan,
                                pk=plan_id,
                            )

                            OrderItem.objects.create(
                                order=order,
                                workout_plan=plan,
                                quantity=quantity,
                            )

                        else:
                            raise ValueError(
                                f"Unknown cart item type: {item_type}"
                            )

                    order.update_total()

                    line_items = []

                    for item in order.items.all():
                        plan = item.plan

                        if plan is None:
                            raise ValueError(
                                "An order item is missing its plan."
                            )

                        unit_amount = int(
                            plan.price * Decimal("100")
                        )

                        line_items.append(
                            {
                                "price_data": {
                                    "currency": "gbp",
                                    "product_data": {
                                        "name": plan.name,
                                    },
                                    "unit_amount": unit_amount,
                                },
                                "quantity": item.quantity,
                            }
                        )

                    success_url = request.build_absolute_uri(
                        reverse(
                            "payments:checkout_success",
                            kwargs={
                                "order_number": order.order_number,
                            },
                        )
                    )

                    success_url += (
                        "?session_id={CHECKOUT_SESSION_ID}"
                    )

                    cancel_url = request.build_absolute_uri(
                        reverse("cart:view_cart")
                    )

                    checkout_session = (
                        stripe.checkout.Session.create(
                            mode="payment",
                            payment_method_types=["card"],
                            customer_email=order.email,
                            line_items=line_items,
                            client_reference_id=order.order_number,
                            metadata={
                                "order_number": order.order_number,
                            },
                            success_url=success_url,
                            cancel_url=cancel_url,
                        )
                    )

                    order.stripe_pid = checkout_session.id
                    order.save(
                        update_fields=["stripe_pid"]
                    )

            except stripe.StripeError:
                messages.error(
                    request,
                    "Stripe could not start the payment. "
                    "Please try again.",
                )
                return redirect("payments:checkout")

            except ValueError:
                messages.error(
                    request,
                    "There was a problem processing your cart.",
                )
                return redirect("cart:view_cart")

            return redirect(
                checkout_session.url,
                code=303,
            )

    else:
        initial_data = {
            "email": request.user.email,
        }

        profile = CustomerProfile.objects.filter(
            user=request.user
        ).first()

        if profile:
            initial_data["full_name"] = profile.full_name
            initial_data["email"] = profile.email

        else:
            full_name = request.user.get_full_name()

            if full_name:
                initial_data["full_name"] = full_name
            else:
                initial_data["full_name"] = request.user.username

        order_form = OrderForm(
            initial=initial_data
        )

    context = {
        "order_form": order_form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    }

    return render(
        request,
        "payments/checkout.html",
        context,
    )


@login_required
def checkout_success(request, order_number):
    """
    Verify the Stripe Checkout Session and display the
    successful order page.
    """
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user,
    )

    session_id = request.GET.get("session_id")

    if not session_id:
        messages.error(
            request,
            "The payment session could not be verified.",
        )
        return redirect("nutrition_home")

    try:
        checkout_session = (
            stripe.checkout.Session.retrieve(
                session_id
            )
        )

    except stripe.StripeError:
        messages.error(
            request,
            "The payment could not be verified.",
        )
        return redirect("nutrition_home")

    try:
        stripe_order_number = (
            checkout_session.metadata[
                "order_number"
            ]
        )

    except (KeyError, TypeError):
        messages.error(
            request,
            "The Stripe order information is missing.",
        )
        return redirect("nutrition_home")

    if stripe_order_number != order.order_number:
        messages.error(
            request,
            "The payment does not match this order.",
        )
        return redirect("nutrition_home")

    if checkout_session.payment_status != "paid":
        messages.warning(
            request,
            "Your payment has not been completed.",
        )
        return redirect("cart:view_cart")

    request.session.pop("cart", None)
    request.session.modified = True

    messages.success(
        request,
        "Your payment was successful. Thank you!",
    )

    context = {
        "order": order,
        "checkout_session": checkout_session,
    }

    return render(
        request,
        "payments/checkout_success.html",
        context,
    )