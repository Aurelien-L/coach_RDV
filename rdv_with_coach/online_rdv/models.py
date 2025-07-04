from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Seance(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seances_client")
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seances_coach")
    date = models.DateField()
    heure_debut = models.TimeField()
    objet = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RDV {self.date} {self.heure_debut} - {self.client.username} avec {self.coach.username}"
    
    class Meta:
        unique_together = ["coach", "date", "heure_debut"]  # pour éviter les doublons pour un même coach

    @property
    def heure_fin(self):
        dt_debut = datetime.combine(self.date, self.heure_debut)
        dt_fin = dt_debut + timedelta(minutes=50)
        return dt_fin.time()