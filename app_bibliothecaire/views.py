import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from .models import Membre, Livre, DVD, CD, JeuDePlateau
from itertools import chain

logger = logging.getLogger('app_mediatheque')

# Page de connexion
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('liste_emprunts')
        else:
            return render(request, 'login.html', {'error_message': 'Identifiants incorrects'})
    return render(request, 'login.html')

# Déconnexion
def custom_logout(request):
    logout(request)
    return render(request, 'logout.html')

# Liste des membres
def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'liste_membres.html', {'membres': membres})

# Ajout d’un membre
def ajout_membre(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email', None)
        if nom:
            Membre.objects.create(nom=nom, email=email)
            return redirect('liste_membres')
    return render(request, 'ajout_membre.html')

# Suppression d’un membre
def supprimer_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    membre.delete()
    return HttpResponseRedirect(reverse('liste_membres'))

# Liste des médias
def liste_medias(request):
    medias = {
        'livres': Livre.objects.all(),
        'dvds': DVD.objects.all(),
        'cds': CD.objects.all(),
        'jeux': JeuDePlateau.objects.all()
    }
    return render(request, 'liste_medias.html', medias)

# Ajout d’un média générique
def ajouter_media(request, media_class, template_name):
    if request.method == 'POST':
        fields = {key: request.POST.get(key) for key in request.POST}
        media_class.objects.create(**fields)
        return redirect('liste_medias')
    return render(request, template_name)

def ajouter_livre(request):
    return ajouter_media(request, Livre, 'ajouter_livre.html')

def ajouter_dvd(request):
    return ajouter_media(request, DVD, 'ajouter_dvd.html')

def ajouter_cd(request):
    return ajouter_media(request, CD, 'ajouter_cd.html')

def ajouter_jeu_de_plateau(request):
    return ajouter_media(request, JeuDePlateau, 'ajouter_jeu_de_plateau.html')

# Liste des emprunts
def liste_emprunts(request):
    livres = Livre.objects.filter(disponible=False)
    dvds = DVD.objects.filter(disponible=False)
    cds = CD.objects.filter(disponible=False)

    # Fusionner les résultats sans erreur
    emprunts = list(chain(livres, dvds, cds))

    return render(request, 'liste_emprunts.html', {'emprunts': emprunts})

# Emprunter un média
def emprunter_media(request, media_type, media_id):
    media_classes = {'livre': Livre, 'dvd': DVD, 'cd': CD}
    media = get_object_or_404(media_classes[media_type], id=media_id)

    if request.method == 'POST':
        membre_id = request.POST.get('membre_id')
        membre = get_object_or_404(Membre, id=membre_id)

        if membre.nombre_emprunts_actifs() >= 3:
            return redirect('limite_emprunts')

        if membre.a_un_retard():
            return redirect('emprunts_en_retard')

        if not media.disponible:
            return HttpResponseBadRequest("Ce média est déjà emprunté.")

        # Assigner l'emprunteur
        media.emprunteur = membre
        media.date_emprunt = timezone.now()
        media.disponible = False
        media.save()

        logger.info(f"{membre.nom} a emprunté {media.titre}")
        return redirect('confirmation_emprunt')

    membres = Membre.objects.all()
    return render(request, 'emprunter_media.html', {'membres': membres, 'media': media})

# Retourner un média
def retourner_media(request, emprunt_id):
    """
    Fonction pour rendre un média et le rendre disponible à nouveau.
    """
    # On cherche le média parmi tous les types possibles
    media = None
    for media_class in [Livre, DVD, CD]:
        try:
            media = media_class.objects.get(id=emprunt_id)
            break
        except media_class.DoesNotExist:
            continue

    if not media:
        return HttpResponseBadRequest("Média non trouvé.")

    if not media.emprunteur:
        return HttpResponseBadRequest("Ce média n'est pas actuellement emprunté.")

    # Rendre le média disponible à nouveau
    media.disponible = True
    media.emprunteur = None
    media.date_emprunt = None
    media.save()

    logger.info(f"{media.titre} a été retourné.")
    return redirect('liste_medias')

# Pages d'information
def confirmation_emprunt(request):
    return render(request, 'confirmation_emprunt.html')

def limite_emprunts(request):
    return render(request, 'limite_emprunts.html')

def emprunts_en_retard(request):
    # Trouver tous les emprunts en retard (livres, DVDs, CDs)
    livres_en_retard = Livre.objects.filter(disponible=False, date_emprunt__lt=timezone.now() - timezone.timedelta(days=7))
    dvds_en_retard = DVD.objects.filter(disponible=False, date_emprunt__lt=timezone.now() - timezone.timedelta(days=7))
    cds_en_retard = CD.objects.filter(disponible=False, date_emprunt__lt=timezone.now() - timezone.timedelta(days=7))

    # Récupérer la liste des membres concernés
    membres_en_retard = set()
    for media in list(livres_en_retard) + list(dvds_en_retard) + list(cds_en_retard):
        if media.emprunteur:
            membres_en_retard.add(media.emprunteur)

    return render(request, 'page_des_emprunts_en_retard.html', {'membres': membres_en_retard})


# Modifier un membre
def modifier_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    if request.method == 'POST':
        membre.nom = request.POST.get('nom', membre.nom)
        membre.email = request.POST.get('email', membre.email)
        membre.bloque = request.POST.get('bloque', 'off') == 'on'
        membre.save()
        return redirect('liste_membres')
    return render(request, 'modifier_membre.html', {'membre': membre})

# Suppression d’un livre
def supprimer_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    livre.delete()
    return redirect('liste_medias')

# Suppression d’un DVD
def supprimer_dvd(request, dvd_id):
    dvd = get_object_or_404(DVD, id=dvd_id)
    dvd.delete()
    return redirect('liste_medias')

# Suppression d’un CD
def supprimer_cd(request, cd_id):
    cd = get_object_or_404(CD, id=cd_id)
    cd.delete()
    return redirect('liste_medias')
