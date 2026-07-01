from django.shortcuts import render


def view_cart(request):
    selected_plan = request.GET.get("plan")

    selected_plans = []

    if selected_plan:
        selected_plans.append({
            "name": selected_plan.replace("-", " ").title()
        })

    return render(
        request,
        "cart/cart.html",
        {
            "selected_plans": selected_plans
        },
    )