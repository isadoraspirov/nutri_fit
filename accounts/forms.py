import re

from django import forms
from django.core.exceptions import ValidationError

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

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()

        if len(full_name) < 2:
            raise ValidationError(
                "Please enter a valid full name."
            )

        allowed_characters = all(
            character.isalpha()
            or character in " -'"
            for character in full_name
        )

        if not allowed_characters:
            raise ValidationError(
                "The name can only contain letters, spaces, "
                "apostrophes and hyphens."
            )

        return full_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get(
            "phone_number",
            "",
        ).strip()

        if not phone_number:
            return phone_number

        if not re.fullmatch(
            r"[0-9+\s().-]+",
            phone_number,
        ):
            raise ValidationError(
                "Enter a valid phone number."
            )

        digit_count = sum(
            character.isdigit()
            for character in phone_number
        )

        if digit_count < 7 or digit_count > 15:
            raise ValidationError(
                "The phone number must contain between "
                "7 and 15 digits."
            )

        return phone_number

    def clean_address_line_1(self):
        address = self.cleaned_data[
            "address_line_1"
        ].strip()

        if len(address) < 5:
            raise ValidationError(
                "Please enter a complete address."
            )

        return address

    def clean_town_or_city(self):
        town_or_city = self.cleaned_data[
            "town_or_city"
        ].strip()

        if len(town_or_city) < 2:
            raise ValidationError(
                "Please enter a valid town or city."
            )

        allowed_characters = all(
            character.isalpha()
            or character in " -'"
            for character in town_or_city
        )

        if not allowed_characters:
            raise ValidationError(
                "The town or city can only contain letters, "
                "spaces, apostrophes and hyphens."
            )

        return town_or_city

    def clean_postcode(self):
        postcode = self.cleaned_data[
            "postcode"
        ].strip().upper()

        if not re.fullmatch(
            r"[A-Z0-9 -]{3,20}",
            postcode,
        ):
            raise ValidationError(
                "Please enter a valid postcode."
            )

        return postcode

    def clean_country(self):
        country = self.cleaned_data[
            "country"
        ].strip()

        if len(country) < 2:
            raise ValidationError(
                "Please enter a valid country."
            )

        allowed_characters = all(
            character.isalpha()
            or character in " -'"
            for character in country
        )

        if not allowed_characters:
            raise ValidationError(
                "The country can only contain letters, "
                "spaces, apostrophes and hyphens."
            )

        return country