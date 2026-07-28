import uuid

from django.db import models

from nutrition.models import NutritionPlan
from workouts.models import WorkoutPlan


class Order(models.Model):
    order_number = models.CharField(
        max_length=32,
        unique=True,
        editable=False,
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    stripe_pid = models.CharField(
        max_length=254,
        blank=True,
    )

    def _generate_order_number(self):
        """Generate a random unique order number."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update the total cost of the order."""
        total = sum(
            item.line_total
            for item in self.items.all()
        )

        self.order_total = total
        self.save(update_fields=["order_total"])

    def save(self, *args, **kwargs):
        """Generate an order number before saving."""
        if not self.order_number:
            self.order_number = self._generate_order_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
    )

    nutrition_plan = models.ForeignKey(
        NutritionPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    quantity = models.PositiveIntegerField(default=1)

    line_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        default=0,
    )

    @property
    def plan(self):
        """Return the nutrition or workout plan."""
        return self.nutrition_plan or self.workout_plan

    def save(self, *args, **kwargs):
        """Calculate the line total before saving."""
        plan = self.plan

        if plan is None:
            raise ValueError(
                "An order item must have either a nutrition "
                "plan or a workout plan."
            )

        if self.nutrition_plan and self.workout_plan:
            raise ValueError(
                "An order item cannot contain both a nutrition "
                "plan and a workout plan."
            )

        self.line_total = plan.price * self.quantity

        super().save(*args, **kwargs)

        self.order.update_total()

    def delete(self, *args, **kwargs):
        """Update the order total after removing an item."""
        order = self.order

        super().delete(*args, **kwargs)

        order.update_total()

    def __str__(self):
        plan_name = self.plan.name if self.plan else "Deleted plan"

        return (
            f"{plan_name} "
            f"({self.order.order_number})"
        )