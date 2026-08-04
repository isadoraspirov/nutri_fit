from django import forms

from .models import CustomerProfile


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile

        fields = [
            "full_name",
            "email",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "town_or_city",
            "postcode",
            "country",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your full name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email address",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                }
            ),
            "address_line_1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your address",
                }
            ),
            "address_line_2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Apartment, suite or building",
                }
            ),
            "town_or_city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your town or city",
                }
            ),
            "postcode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your postcode",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your country",
                }
            ),
        }
