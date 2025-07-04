from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard') # A VERIFIER
        else:
            messages.info(request, "Identifiant ou mot de passe incorrect")

    form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect('accueil') # A VERIFIER


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
        return render(request, 'accounts/dashboard_coach.html', {'user': user})
    else:
        return render(request, 'accounts/dashboard_client.html', {'user': user})