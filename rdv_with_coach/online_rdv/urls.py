from django.urls import path

from . import views

app_name = "online_rdv"

urlpatterns = [
    path('', views.prendre_rdv, name='rdv'),
    path('annuler/<int:seance_id>/', views.annuler_seance, name='annuler_seance'),
    path('historique_coach/', views.historique_coach, name='historique_coach'),
    path('historique_client/', views.historique_client, name='historique_client'),
    path('historique/', views.redirect_historique, name='historique'),
    path("modifier_note/<int:seance_id>/", views.modifier_note_coach, name="modifier_note_coach"),
    path("seance/<int:seance_id>/", views.seance_detail, name="seance_detail"),
]
