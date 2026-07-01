def cart_contents(request):

    selected_plans = request.session.get("selected_plans", [])

    return {
        "selected_plans": selected_plans,
        "plan_count": len(selected_plans),
    }
