from django import forms
from .models import Seance
from django.contrib.auth.models import User, Group
from datetime import datetime, date as dt_date, time, timedelta

class SeanceForm(forms.ModelForm):
    HEURES_DISPONIBLES = [
        (time(h, 0), f"{h:02d}:00") for h in range(9, 12)
    ] + [
        (time(h, 0), f"{h:02d}:00") for h in range(13, 18)
    ]

    heure_debut = forms.ChoiceField(choices=HEURES_DISPONIBLES, label="Heure du rendez-vous")

    class Meta:
        model = Seance
        fields = ['date', 'heure_debut', 'coach', 'objet']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)

        coach_group = Group.objects.get(name='coach')
        self.fields['coach'].queryset = User.objects.filter(groups=coach_group)

    def clean(self):
        cleaned_data = super().clean()
        date_rdv = cleaned_data.get('date')
        heure_str = cleaned_data.get('heure_debut')
        coach = cleaned_data.get('coach')

        if not (date_rdv and heure_str and coach):
            return cleaned_data

        # Convertir la chaîne de l'heure en objet time
        heure_debut = time.fromisoformat(heure_str)

        # Vérifier que la date n’est pas passée
        today = dt_date.today()
        if date_rdv < today:
            self.add_error('date', "Vous ne pouvez pas prendre rendez-vous à une date passée.")
            return cleaned_data
        
        # Empêcher les rendez-vous le week-end
        if date_rdv.weekday() >= 5:
            self.add_error('date', "Les rendez-vous ne sont pas disponibles le week-end.")
            return cleaned_data

        # Si aujourd’hui, vérifier que l’heure choisie n’est pas dépassée
        now = datetime.now()
        if date_rdv == today and heure_debut <= now.time():
            self.add_error('heure_debut', "Cette heure est déjà passée.")
            return cleaned_data

        # Calcul de l'heure de fin
        heure_fin = (datetime.combine(date_rdv, heure_debut) + timedelta(minutes=50)).time()

        # Vérifier qu'il n'y a pas de chevauchement avec d'autres séances du coach
        seances = Seance.objects.filter(coach=coach, date=date_rdv)

        for seance in seances:
            debut = seance.heure_debut
            fin = (datetime.combine(seance.date, debut) + timedelta(minutes=50)).time()

            if not (heure_fin <= debut or heure_debut >= fin):
                self.add_error('heure_debut', "Ce créneau chevauche une autre séance pour ce coach.")
                break

        return cleaned_data