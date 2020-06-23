from django.shortcuts import render
from .models import Customer, StageChoice


def doctors(request):
    doctors = Customer.objects.filter(stage__name=StageChoice.CLINIC)
    return render(request, "customer/doctors_list.html", {"doctors": doctors})

