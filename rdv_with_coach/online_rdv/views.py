from django.shortcuts import render, redirect
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
            return redirect('dashboard')
    else:
        form = SeanceForm(client=request.user)

    return render(request, 'online_rdv/prise_rdv.html', {'form': form})