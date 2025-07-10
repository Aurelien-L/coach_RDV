from django.urls import path

from . import views

app_name = "online_rdv"

urlpatterns = [
    path('', views.prendre_rdv, name='rdv'),    # URL pour la prise de RDV
    path('annuler/<int:seance_id>/', views.annuler_seance, name='annuler_seance'),      # route annulant un RDV
    path('historique_coach/', views.historique_coach, name='historique_coach'),     # URL vers l'historique du coach
    path('historique_client/', views.historique_client, name='historique_client'),      # URL vers l'historique du client
    path('historique/', views.redirect_historique, name='historique'),      # route redirigeant vers l'historique associé à l'utilisateur connecté
    path("modifier_note/<int:seance_id>/", views.modifier_note_coach, name="modifier_note_coach"),      # URL vers la modification d'une note (coach)
    path("seance/<int:seance_id>/", views.seance_detail, name="seance_detail"),     # URL vers le détail d'une séance
]
