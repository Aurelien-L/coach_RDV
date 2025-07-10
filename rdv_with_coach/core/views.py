from django.shortcuts import render
from django.contrib.auth.models import Group


def accueil(request):
    """
    Vue redirigeant vers la page d'accueil
    
    """
    return render(request, 'core/accueil.html')
