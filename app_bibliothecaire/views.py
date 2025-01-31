from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Membre, Livre, DVD, CD, JeuDePlateau, Emprunt

# Afficher la liste des membres
def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'app_membre/liste_membres.html', {'membres': membres})


# Ajouter un membre
def ajout_membre(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        if nom and email:  # Vérification des champs requis
            Membre.objects.create(nom=nom, email=email)
            return redirect('liste_membres')
    return render(request, 'app_membre/ajout_membre.html')


# Supprimer un membre
def supprimer_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    membre.delete()
    return redirect('liste_membres')


# Afficher la liste des médias
def liste_medias(request):
    livres = Livre.objects.all()
    cds = CD.objects.all()
    dvds = DVD.objects.all()
    jeux = JeuDePlateau.objects.all()
    return render(request, 'app_membre/liste_media.html', {
        'livres': livres, 'cds': cds, 'dvds': dvds, 'jeux': jeux
    })


# Ajouter un média (livre, dvd, cd, jeu de plateau)
def ajouter_media(request, media_type):
    if request.method == 'POST':
        titre = request.POST.get('titre')  # Correction : nom → titre

        media_classes = {
            'livre': (Livre, 'auteur'),
            'dvd': (DVD, 'realisateur'),
            'cd': (CD, 'artiste'),
            'jeu': (JeuDePlateau, 'createur'),
        }

        if media_type in media_classes:
            media_class, champ_specifique = media_classes[media_type]
            champ_valeur = request.POST.get(champ_specifique, "")

            if titre and champ_valeur:  # Vérification des champs requis
                media_class.objects.create(
                    titre=titre, **{champ_specifique: champ_valeur}
                )
                return redirect('liste_medias')

    return render(request, 'app_membre/ajouter_media.html', {'media_type': media_type})


# Supprimer un média
def supprimer_media(request, media_id, media_type):
    media_classes = {'livre': Livre, 'dvd': DVD, 'cd': CD, 'jeu': JeuDePlateau}
    media_class = media_classes.get(media_type)

    if media_class:
        media = get_object_or_404(media_class, id=media_id)
        media.delete()

    return redirect('liste_medias')


# Afficher la liste des emprunts
def liste_emprunts(request):
    emprunts = Emprunt.objects.all()
    return render(request, 'app_membre/liste_emprunts.html', {'emprunts': emprunts})


# Emprunter un média
def emprunter_media(request, media_type, media_id):
    media_models = {'livre': Livre, 'dvd': DVD, 'cd': CD}
    media_class = media_models.get(media_type)

    if not media_class:
        return redirect('liste_medias')

    media = get_object_or_404(media_class, id=media_id)

    membre = request.user  # Modifier pour récupérer l'utilisateur connecté

    if media.disponible and membre.peut_emprunter():
        Emprunt.objects.create(membre=membre, media=media, date_emprunt=timezone.now())
        media.disponible = False
        media.save()
        return redirect('liste_emprunts')

    return redirect('liste_medias')


# Retourner un média
def retourner_media(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)

    # Marquer le média comme disponible
    emprunt.media.disponible = True
    emprunt.media.save()

    # Enregistrer la date de retour
    emprunt.date_retour = timezone.now()
    emprunt.save()

    return redirect('liste_emprunts')

