from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('coach', 'Coach'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        label="Je suis", 
        widget=forms.RadioSelect
        )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']