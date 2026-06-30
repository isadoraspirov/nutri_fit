from django.db import models

# Create your models here.

class WorkoutPlan(models.Model):

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    level = models.CharField(
        max_length=50
    )

    image = models.ImageField(
        upload_to="workouts/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name