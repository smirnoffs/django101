from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    name = models.CharField(max_length=120)
    stage = models.ForeignKey("customer.Stage", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.stage})"

class StageChoice(models.TextChoices):
    CLINIC = "CL", _("Clinic")
    PRECLINIC = "PC", _("Preclinic")

class Stage(models.Model):
    name = models.CharField(max_length=120, choices=StageChoice.choices)

    def __str__(self):
        return self.name