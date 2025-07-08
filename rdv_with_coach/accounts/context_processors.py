from django.contrib.auth.models import Group

def is_coach(request):
    is_coach = False
    if request.user.is_authenticated:
        is_coach = request.user.groups.filter(name='coach').exists()
    return {'is_coach': is_coach}