from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "full_name": "Full Name",
            "email": "Email Address",
        }

        self.fields["full_name"].widget.attrs["autofocus"] = True

        for field_name, field in self.fields.items():
            placeholder = placeholders[field_name]

            if field.required:
                placeholder += " *"

            field.widget.attrs["placeholder"] = placeholder
            field.widget.attrs["class"] = "form-control"
            field.label = False