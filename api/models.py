from django.db import models

class Meal(models.Model):
    name = models.CharField(max_length=255)
    nutrients = models.JSONField()  # Store nutrient data in JSON format

    def __str__(self):
        return self.name
