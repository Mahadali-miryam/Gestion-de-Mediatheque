import logging
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import Membre, Livre, DVD, CD, JeuDePlateau, Emprunt
from .forms import Creationmembre
from django.contrib import messages

logger = logging.getLogger('app_mediatheque')


# 🔹 Déconnexion
def custom_logout(request):
    logout(request)
    return render(request, 'logout.html')


# 🔹 Connexion utilisateur
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


# 🔹 Liste des membres
def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'liste_membres.html', {'membres': membres})


# 🔹 Ajouter un membre
def ajout_membre(request):
    if request.method == 'POST':
        form = Creationmembre(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_membres')
    else:
        form = Creationmembre()
    return render(request, 'ajout_membre.html', {'form': form})


# 🔹 Modifier un membre
def modifier_membre(request, membre_id):
    membre = get_object_or_404(Membre, pk=membre_id)
    if request.method == 'POST':
        membre.nom = request.POST.get('nom', membre.nom)
        membre.email = request.POST.get('email', membre.email)
        membre.bloque = request.POST.get('bloque', 'off') == 'on'
        membre.save()
        return redirect('liste_membres')
    return render(request, 'modifier_membre.html', {'membre': membre})


# 🔹 Supprimer un membre
def supprimer_membre(request, membre_id):
    membre = get_object_or_404(Membre, pk=membre_id)
    membre.delete()
    return redirect('liste_membres')


# 🔹 Liste des médias
def liste_medias(request):
    return render(request, 'liste_medias.html', {
        'livres': Livre.objects.all(),
        'dvds': DVD.objects.all(),
        'cds': CD.objects.all(),
        'jeux': JeuDePlateau.objects.all()
    })  # ✅ Correction ici


# 📚 Liste des livres
def liste_livres(request):
    livres = Livre.objects.all()
    return render(request, 'livres.html', {'livres': livres})


# 🎵 Liste des CDs
def liste_cds(request):
    cds = CD.objects.all()
    return render(request, 'cds.html', {'cds': cds})


# 🎬 Liste des DVDs
def liste_dvds(request):
    dvds = DVD.objects.all()
    return render(request, 'dvds.html', {'dvds': dvds})


# 🎲 Liste des jeux de plateau
def liste_jeux(request):
    jeux = JeuDePlateau.objects.all()
    return render(request, 'jeuxdeplateau.html', {'jeux': jeux})



# 🔹 Ajouter des médias
def ajouter_livre(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        auteur = request.POST.get('auteur')
        if titre and auteur:
            Livre.objects.create(titre=titre, auteur=auteur)
            return redirect('liste_livres')
    return render(request, 'ajouter_livre.html')


def ajouter_dvd(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        realisateur = request.POST.get('realisateur')
        if titre and realisateur:
            DVD.objects.create(titre=titre, realisateur=realisateur)
            return redirect('liste_dvds')
    return render(request, 'ajouter_dvd.html')


def ajouter_cd(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        artiste = request.POST.get('artiste')
        if titre and artiste:
            CD.objects.create(titre=titre, artiste=artiste)
            return redirect('liste_cds')
    return render(request, 'ajouter_cd.html')


def ajouter_jeu_de_plateau(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        createur = request.POST.get('createur')
        if titre and createur:
            JeuDePlateau.objects.create(titre=titre, createur=createur)
            return redirect('liste_jeux')
    return render(request, 'ajouter_jeu_de_plateau.html')


# 🔹 Suppression d’un média
def supprimer_media(request, media_type, media_id):
    if media_type == 'livre':
        media = get_object_or_404(Livre, id=media_id)
    elif media_type == 'dvd':
        media = get_object_or_404(DVD, id=media_id)
    elif media_type == 'cd':
        media = get_object_or_404(CD, id=media_id)
    else:
        messages.error(request, "Type de média invalide.")
        return redirect('liste_medias')

    media.delete()
    messages.success(request, f"{media_type.capitalize()} supprimé avec succès !")
    return redirect('liste_medias')

# 🔹 Liste des emprunts
def liste_emprunts(request):
    emprunts = Emprunt.objects.select_related('membre').all()

    # Dictionnaire pour retrouver le bon média selon le type
    media_classes = {
        "livre": Livre,
        "dvd": DVD,
        "cd": CD
    }

    for emprunt in emprunts:
        try:
            media_class = media_classes.get(emprunt.media_type)
            if media_class:
                media_obj = media_class.objects.filter(id=emprunt.media_id).first()
                emprunt.media_titre = media_obj.titre if media_obj else "Média introuvable"
            else:
                emprunt.media_titre = "Type inconnu"
        except Exception as e:
            emprunt.media_titre = f"Erreur : {e}"

    print("DEBUG - Emprunts trouvés :", list(emprunts))  # Vérification dans la console

    return render(request, 'liste_emprunts.html', {'emprunts': emprunts})



# 🔹 Emprunter un média
def emprunter_media(request, media_type, media_id):
    """Permet à un membre d'emprunter un livre, un DVD ou un CD avec des restrictions."""

    # Définition des types de médias valides
    media_classes = {'livre': Livre, 'dvd': DVD, 'cd': CD}

    if media_type not in media_classes:
        return HttpResponseBadRequest("❌ Type de média invalide.")

    # Récupération du média
    media = get_object_or_404(media_classes[media_type], pk=media_id)

    if request.method == 'POST':
        membre_id = request.POST.get('membre_id')
        membre = get_object_or_404(Membre, pk=membre_id)

        # Vérifications
        if Emprunt.objects.filter(membre=membre).count() >= 3:
            return HttpResponseBadRequest("⚠️ Vous avez atteint la limite de 3 emprunts.")
        if Emprunt.objects.filter(membre=membre, media_type=media_type, media_id=media_id).exists():
            return HttpResponseBadRequest("⚠️ Vous avez déjà emprunté ce média.")
        if not media.disponible:
            return HttpResponseBadRequest("⚠️ Ce média est déjà emprunté.")

        # Création de l’emprunt
        nouvel_emprunt = Emprunt.objects.create(
            membre=membre,
            media_type=media_type,
            media_id=media_id,
            date_emprunt=timezone.now(),
            date_retour=timezone.now() + timedelta(days=7)
        )

        # Marquer le média comme non disponible
        media.disponible = False
        media.save()

        logger.info(f"{membre.nom} a emprunté {media_type} (ID: {media_id})")
        print(f"DEBUG: {membre.nom} a emprunté {media.titre} ({media_type}) jusqu'au {nouvel_emprunt.date_retour}")

        return redirect('confirmation_emprunt')

    # Vérifie si la liste des médias est bien envoyée au template
    medias_disponibles = media_classes[media_type].objects.filter(disponible=True)

    return render(request, 'emprunter_media.html', {
        'membres': Membre.objects.all(),
        'medias': medias_disponibles,  # ✅ Vérifie que cette variable est bien passée au template
        'media_type': media_type,
    })


# 🔹 Retourner un média
def retourner_media(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, pk=emprunt_id)
    media_classes = {'livre': Livre, 'dvd': DVD, 'cd': CD}
    media = get_object_or_404(media_classes[emprunt.media_type], pk=emprunt.media_id)

    # Supprimer l'emprunt
    emprunt.delete()

    # Vérifier s'il reste des emprunts actifs pour ce média
    emprunts_restant = Emprunt.objects.filter(media_type=emprunt.media_type, media_id=emprunt.media_id).exists()

    # Mettre à jour la disponibilité du média
    media.disponible = not emprunts_restant
    media.save()
    # Vérifier si le livre est encore emprunté
    livre = get_object_or_404(Livre, pk=emprunt.media_id)
    emprunts_restant = Emprunt.objects.filter(media_type="livre", media_id=livre.id).exists()
    livre.disponible = not emprunts_restant
    livre.save()

    logger.info(f"{emprunt.membre.nom} a retourné un {emprunt.media_type} (ID: {emprunt.media_id})")
    return redirect('liste_emprunts')

# 🔹 Pages d’information
def confirmation_emprunt(request):
    return render(request, 'confirmation_emprunt.html')



def emprunts_en_retard(request):
    emprunts = Emprunt.objects.filter(date_retour__lt=timezone.now())
    return render(request, 'page_des_emprunts_en_retard.html', {'emprunts': emprunts})

def limite_emprunts(request):
    emprunts = Emprunt.objects.select_related('membre').all()
    return render(request, 'limite_emprunts.html',)
