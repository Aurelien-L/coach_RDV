from django.urls import path
from .views import accueil

from . import views

#app_name = "accueil"

urlpatterns = [
    path('', accueil, name='accueil'),  # Vue accueil : accès = "/"
]
