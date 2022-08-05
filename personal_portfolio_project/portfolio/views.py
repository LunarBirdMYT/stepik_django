from django.shortcuts import render
from .models import Project

def home(request):
    projects = Project.objects.all()
    template = 'portfolio/home.html'
    return render(request, template, {'projects': projects})
