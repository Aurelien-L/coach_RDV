from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from online_rdv.models import Seance
from django.utils import timezone



def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            messages.info(request, "Identifiant ou mot de passe incorrect")

    form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect('accueil')


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            user.save()

            # Ajouter l'utilisateur au groupe correspondant
            group = Group.objects.get(name=role)
            user.groups.add(group)

            messages.success(request, "Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.")
            return redirect('accounts:login')
    
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user

    if user.groups.filter(name='coach').exists():
        seances = Seance.objects.filter(coach=user,  date__gte=timezone.now().date()).order_by('date', 'heure_debut')
        return render(request, 'accounts/dashboard_coach.html', {'user': user, 'seances': seances})
    else:
        seances = Seance.objects.filter(client=user,  date__gte=timezone.now().date()).order_by('date', 'heure_debut')
        return render(request, 'accounts/dashboard_client.html', {'user': user, 'seances': seances})