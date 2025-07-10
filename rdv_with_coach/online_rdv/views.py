from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SeanceForm
from .models import Seance
from .forms import NoteCoachForm
from django.utils import timezone

@login_required
def prendre_rdv(request):
    """
    Vue permettant la prise d'un RDV (nécessite que l'utilisateur soit connecté)

    """
    if request.method == 'POST':
        form = SeanceForm(request.POST, client=request.user)
        if form.is_valid():
            seance = form.save(commit=False)
            seance.client = request.user
            seance.save()
            messages.success(request, "Votre rendez-vous a bien été pris en compte !")
            return redirect('accounts:dashboard')
    else:
        form = SeanceForm(client=request.user)

    return render(request, 'online_rdv/prise_rdv.html', {'form': form})


@login_required
def annuler_seance(request, seance_id):
    """
    Vue permettant d'annuler une séance (nécessite que l'utilisateur soit connecté)

    """
    user = request.user

    # Recherche filtrée selon le rôle de l'utilisateur
    if user.groups.filter(name='client').exists():
        seance = get_object_or_404(Seance, id=seance_id, client=user)
    elif user.groups.filter(name='coach').exists():
        seance = get_object_or_404(Seance, id=seance_id, coach=user)
    else:
        return redirect('accounts:dashboard')  # utilisateur non autorisé

    if request.method == 'POST':
        seance.delete()
        if user.groups.filter(name='client').exists():
            return redirect('accounts:dashboard')
        else:
            return redirect('accounts:dashboard')

    return redirect('accounts:dashboard')


@login_required
def historique_coach(request):
    """
    Vue de l'historique du coach (nécessite que l'utilisateur soit connecté et soit du groupe "coach")

    """
    if not request.user.groups.filter(name='coach').exists():
        return redirect('accounts:dashboard')
    
    seances = Seance.objects.filter(coach=request.user, date__lt=timezone.now().date()).order_by('-date')
    return render(request, 'online_rdv/historique_coach.html', {'seances': seances})


@login_required
def modifier_note_coach(request, seance_id):
    """
    Vue permettant au coach de modifier une note sur une séance passée

    """
    if not request.user.groups.filter(name='coach').exists():
        return redirect('accounts:dashboard')

    seance = get_object_or_404(Seance, id=seance_id, coach=request.user)

    if request.method == 'POST':
        form = NoteCoachForm(request.POST, instance=seance)
        if form.is_valid():
            form.save()
    return redirect('online_rdv:historique_coach')


@login_required
def historique_client(request):
    """
    Vue de l'historique du client (nécessite que l'utilisateur soit connecté et soit du groupe "client")

    """
    if not request.user.groups.filter(name='client').exists():
        return redirect('dashboard_coach')

    seances = Seance.objects.filter(client=request.user, date__lt=timezone.now().date()).order_by('-date')
    return render(request, 'online_rdv/historique_client.html', {'seances': seances})


@login_required
def redirect_historique(request):
    """
    Vue redirigeant vers la route correspondant à l'historique de l'utilisateur connecté

    """
    if request.user.groups.filter(name='coach').exists():
        return redirect('online_rdv:historique_coach')
    elif request.user.groups.filter(name='client').exists():
        return redirect('online_rdv:historique_client')
    else:
        return redirect('Accueil') 
    

@login_required
def seance_detail(request, seance_id):
    """
    Vue permettant d'accéder aux détails d'une séance

    """
    seance = get_object_or_404(Seance, id=seance_id)

    if request.user.groups.filter(name='client').exists():
        if seance.client != request.user:
            return redirect('online_rdv:historique_client')
    elif request.user.groups.filter(name='coach').exists():
        if seance.coach != request.user:
            return redirect('online_rdv:historique_coach')
    else:
        return redirect('Accueil')
    
    if request.method == "POST" and request.user.groups.filter(name='coach').exists():
        note = request.POST.get("note_coach", "")
        seance.note_coach = note
        seance.save()
        messages.success(request, "✅ Note enregistrée avec succès.")
        return redirect('online_rdv:seance_detail', seance_id=seance.id)
    
    return render(request, 'online_rdv/seance_detail.html', {'seance': seance})