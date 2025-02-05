from django.db import models
from django.utils import timezone
from datetime import timedelta

# Fonction pour la date de retour par défaut (7 jours après l'emprunt)
def date_retour_defaut():
    return timezone.now() + timedelta(days=7)

# Modèle pour les membres
class Membre(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    bloque = models.BooleanField(default=False)  # Empêche d'emprunter en cas de problème
    objects = models.Manager()

    def __str__(self):
        return self.nom

    def nombre_emprunts_actifs(self):
        """Retourne le nombre d'emprunts en cours (non rendus)"""
        return (
            Livre.objects.filter(emprunteur=self, disponible=False).count() +
            DVD.objects.filter(emprunteur=self, disponible=False).count() +
            CD.objects.filter(emprunteur=self, disponible=False).count()
        )

    def a_un_retard(self):
        """Vérifie si le membre a un emprunt en retard"""
        return (
            Livre.objects.filter(emprunteur=self, disponible=False, date_emprunt__lt=timezone.now() - timedelta(days=7)).exists() or
            DVD.objects.filter(emprunteur=self, disponible=False, date_emprunt__lt=timezone.now() - timedelta(days=7)).exists() or
            CD.objects.filter(emprunteur=self, disponible=False, date_emprunt__lt=timezone.now() - timedelta(days=7)).exists()
        )

    def peut_emprunter(self):
        """Un membre peut emprunter s'il a moins de 3 emprunts actifs et aucun retard"""
        return not self.bloque and not self.a_un_retard() and self.nombre_emprunts_actifs() < 3

# Modèles concrets des médias (Livre, DVD, CD)
class Livre(models.Model):
    titre = models.CharField(max_length=100)
    auteur = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    emprunteur = models.ForeignKey(Membre, null=True, blank=True, on_delete=models.SET_NULL)
    date_emprunt = models.DateField(null=True, blank=True)
    date_retour = models.DateField(default=date_retour_defaut, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.titre

class DVD(models.Model):
    titre = models.CharField(max_length=100)
    realisateur = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    emprunteur = models.ForeignKey(Membre, null=True, blank=True, on_delete=models.SET_NULL)
    date_emprunt = models.DateField(null=True, blank=True)
    date_retour = models.DateField(default=date_retour_defaut, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.titre

class CD(models.Model):
    titre = models.CharField(max_length=100)
    artiste = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    emprunteur = models.ForeignKey(Membre, null=True, blank=True, on_delete=models.SET_NULL)
    date_emprunt = models.DateField(null=True, blank=True)
    date_retour = models.DateField(default=date_retour_defaut, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.titre

# Modèle pour les jeux de plateau (NON empruntables)
class JeuDePlateau(models.Model):
    nom = models.CharField(max_length=100)
    createur = models.CharField(max_length=100, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.nom

# Gestion des emprunts et des retours directement dans les modèles Livre, DVD et CD
def emprunter_media(media, membre):
    """
    Fonction pour emprunter un livre, DVD ou CD.
    Vérifie si le membre peut emprunter et met à jour le statut du média.
    """
    if not membre.peut_emprunter():
        raise ValueError("Ce membre a atteint la limite d'emprunts ou a un retard.")

    if not media.disponible:
        raise ValueError(f"Ce {media.__class__.__name__} est déjà emprunté.")

    media.disponible = False
    media.emprunteur = membre
    media.date_emprunt = timezone.now().date()
    media.save()

def rendre_media(media):
    """
    Fonction pour rendre un média et le rendre disponible à nouveau.
    """
    if media.disponible:
        raise ValueError(f"Ce {media.__class__.__name__} n'était pas emprunté.")

    media.disponible = True
    media.emprunteur = None
    media.date_emprunt = None
    media.save()
