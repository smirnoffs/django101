from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer, StageChoice


def doctors(request):
    doctors = Customer.objects.filter(stage__name=StageChoice.CLINIC)
    docs = "".join(f"<li>{doc.name}</li>" for doc in doctors)
    html = f"<html><body><ul>{docs}</ul></body></html>"
    return HttpResponse(html)
