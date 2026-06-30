from django.db import models

# Create your models here.

class NutritionPlan(models.Model):

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="nutrition/",
        blank=True,
        null=True
    )

    duration_weeks = models.IntegerField()

    def __str__(self):
        return self.name