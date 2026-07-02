from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("line_total",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = (
        "order_number",
        "date",
        "order_total",
        "stripe_pid",
    )

    fields = (
        "order_number",
        "full_name",
        "email",
        "date",
        "order_total",
        "stripe_pid",
    )

    inlines = (OrderItemInline,)

    list_display = (
        "order_number",
        "full_name",
        "email",
        "date",
        "order_total",
    )

    ordering = ("-date",)
