from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import CustomerProfileForm
from .models import CustomerProfile


@login_required
def profile_detail(request):
    """
    Display the logged-in user's customer profile.
    """
    profile = CustomerProfile.objects.filter(
        user=request.user
    ).first()

    context = {
        "profile": profile,
    }

    return render(
        request,
        "accounts/profile_detail.html",
        context,
    )


@login_required
def profile_create(request):
    """
    Allow a logged-in user to create their customer profile.
    """
    if CustomerProfile.objects.filter(user=request.user).exists():
        messages.info(
            request,
            "You already have saved account details.",
        )
        return redirect("profile_detail")

    if request.method == "POST":
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            messages.success(
                request,
                "Your account details were saved successfully.",
            )
            return redirect("profile_detail")

    else:
        form = CustomerProfileForm(
            initial={
                "email": request.user.email,
            }
        )

    context = {
        "form": form,
        "page_title": "Add My Details",
        "button_text": "Save Details",
    }

    return render(
        request,
        "accounts/profile_form.html",
        context,
    )


@login_required
def profile_update(request):
    """
    Allow the logged-in user to update their customer profile.
    """
    profile = get_object_or_404(
        CustomerProfile,
        user=request.user,
    )

    if request.method == "POST":
        form = CustomerProfileForm(
            request.POST,
            instance=profile,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your account details were updated successfully.",
            )
            return redirect("profile_detail")

    else:
        form = CustomerProfileForm(
            instance=profile,
        )

    context = {
        "form": form,
        "page_title": "Edit My Details",
        "button_text": "Save Changes",
    }

    return render(
        request,
        "accounts/profile_form.html",
        context,
    )


@login_required
def profile_delete(request):
    """
    Allow the logged-in user to delete their customer profile.
    """
    profile = get_object_or_404(
        CustomerProfile,
        user=request.user,
    )

    if request.method == "POST":
        profile.delete()

        messages.success(
            request,
            "Your account details were deleted successfully.",
        )
        return redirect("profile_detail")

    context = {
        "profile": profile,
    }

    return render(
        request,
        "accounts/profile_confirm_delete.html",
        context,
    )