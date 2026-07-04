import uuid

from django.db import models
from nutrition.models import NutritionPlan


class Order(models.Model):
    order_number = models.CharField(
        max_length=32,
        unique=True,
        editable=False
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    stripe_pid = models.CharField(
        max_length=254,
        blank=True
    )

    def _generate_order_number(self):
        """Generate a random unique order number."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update the total cost of the order."""
        total = sum(item.line_total for item in self.items.all())
        self.order_total = total
        self.save(update_fields=["order_total"])

    def save(self, *args, **kwargs):
        """Set the order number if it hasn't been generated yet."""
        if not self.order_number:
            self.order_number = self._generate_order_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    nutrition_plan = models.ForeignKey(
        NutritionPlan,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False
    )

    def save(self, *args, **kwargs):
        """Automatically calculate the line total."""
        self.line_total = self.nutrition_plan.price * self.quantity
        super().save(*args, **kwargs)

        # Update the parent order total
        self.order.update_total()

    def delete(self, *args, **kwargs):
        """Update the order total when an item is removed."""
        order = self.order
        super().delete(*args, **kwargs)
        order.update_total()

    def __str__(self):
        return f"{self.nutrition_plan.name} ({self.order.order_number})"