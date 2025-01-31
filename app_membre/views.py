from django.shortcuts import render
from .models import Membre

def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'app_membre/liste_membres.html', {'membres': membres})