from decimal import Decimal

from nutrition.models import NutritionPlan
from workouts.models import WorkoutPlan


def cart_contents(request):
    cart = request.session.get("cart", {})

    cart_items = []
    cart_total = Decimal("0.00")
    product_count = 0

    for item_key, quantity in cart.items():
        try:
            item_type, plan_id = item_key.split("_", 1)
            plan_id = int(plan_id)
        except (ValueError, AttributeError):
            continue

        if item_type == "nutrition":
            try:
                plan = NutritionPlan.objects.get(pk=plan_id)
            except NutritionPlan.DoesNotExist:
                continue

        elif item_type == "workout":
            try:
                plan = WorkoutPlan.objects.get(pk=plan_id)
            except WorkoutPlan.DoesNotExist:
                continue

        else:
            continue

        subtotal = plan.price * quantity
        cart_total += subtotal
        product_count += quantity

        cart_items.append(
            {
                "item_key": item_key,
                "item_type": item_type,
                "plan": plan,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return {
        "cart_items": cart_items,
        "cart_total": cart_total,
        "product_count": product_count,
    }