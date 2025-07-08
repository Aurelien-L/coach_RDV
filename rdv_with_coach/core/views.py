from django.shortcuts import render
from django.contrib.auth.models import Group


def accueil(request):
    return render(request, 'core/accueil.html')
