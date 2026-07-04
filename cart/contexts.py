from nutrition.models import NutritionPlan


def cart_contents(request):

    cart = request.session.get("cart", {})
    print("Cart in context:", cart)

    cart_items = []

    total = 0

    for plan_id, quantity in cart.items():

        plan = NutritionPlan.objects.get(pk=plan_id)

        total += plan.price * quantity

        cart_items.append({
            "plan": plan,
            "quantity": quantity,
            "subtotal": plan.price * quantity,
        })

    return {
        "cart_items": cart_items,
        "total": total,
        "plan_count": sum(cart.values()),
    }