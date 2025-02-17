from django.db import models
from django.utils import timezone
from datetime import timedelta

# Fonction pour la date de retour par défaut (7 jours après l'emprunt)
def date_retour_defaut():
    return timezone.now() + timedelta(days=7)

# 🔹 Modèle pour les membres
class Membre(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    bloque = models.BooleanField(default=False)  # Empêche d'emprunter en cas de problème

    objects = models.Manager()

    def __str__(self):
        return self.nom

    def nombre_emprunts_actifs(self):
        """Retourne le nombre d'emprunts en cours (non rendus)"""
        return Emprunt.objects.filter(membre=self, date_retour__isnull=True).count()

    def a_un_retard(self):
        """Vérifie si le membre a un emprunt en retard"""
        return Emprunt.objects.filter(membre=self, date_retour__lt=timezone.now(), date_retour__isnull=False).exists()

    def peut_emprunter(self):
        """Un membre peut emprunter s'il a moins de 3 emprunts actifs et aucun retard"""
        return not self.bloque and not self.a_un_retard() and self.nombre_emprunts_actifs() < 3


# 🔹 Modèles pour les médias (Livre, DVD, CD)
class Livre(models.Model):
    titre = models.CharField(max_length=100)
    auteur = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    date_emprunt = models.DateTimeField(null=True, blank=True)
    emprunteur = models.ForeignKey(Membre, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.titre


class DVD(models.Model):
    titre = models.CharField(max_length=100)
    realisateur = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    date_emprunt = models.DateTimeField(null=True, blank=True)
    emprunteur = models.ForeignKey(Membre, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.titre


class CD(models.Model):
    titre = models.CharField(max_length=100)
    artiste = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    date_emprunt = models.DateTimeField(null=True, blank=True)
    emprunteur = models.ForeignKey(Membre, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.titre


# 🔹 Modèle pour les jeux de plateau (NON empruntables)
class JeuDePlateau(models.Model):
    nom = models.CharField(max_length=100)
    createur = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.nom

# 🔹 Modèle pour les emprunts
class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name="emprunts")
    media_type = models.CharField(max_length=10, choices=[
        ('livre', 'Livre'),
        ('dvd', 'DVD'),
        ('cd', 'CD'),
    ])
    media_id = models.PositiveIntegerField()
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField(default=date_retour_defaut, null=True, blank=True)

    objects = models.Manager()