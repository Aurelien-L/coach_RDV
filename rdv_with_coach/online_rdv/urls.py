from django.urls import path

from . import views

app_name = "online_rdv"

urlpatterns = [
    path('', views.prendre_rdv, name='rdv'),
]
