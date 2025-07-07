from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SeanceForm
from .models import Seance

@login_required
def prendre_rdv(request):
    if request.method == 'POST':
        form = SeanceForm(request.POST, client=request.user)
        if form.is_valid():
            seance = form.save(commit=False)
            seance.client = request.user
            seance.save()
            return redirect('accounts:dashboard')
    else:
        form = SeanceForm(client=request.user)

    return render(request, 'online_rdv/prise_rdv.html', {'form': form})


@login_required
def annuler_seance(request, seance_id):
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