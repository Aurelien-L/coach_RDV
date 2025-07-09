from django.urls import path
from .views import accueil

from . import views

urlpatterns = [
    path('', accueil, name='accueil'),  # Vue accueil : accès = "/"
]
