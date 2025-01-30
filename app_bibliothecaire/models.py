from django.db import models
from django.utils import timezone
from datetime import timedelta

#  Fonction pour la date de retour par défaut (7 jours après l'emprunt)
def date_retour_defaut():
    return timezone.now() + timedelta(days=7)

# Modèle pour les membres
class Membre(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bloque = models.BooleanField(default=False)  # Empêche d'emprunter en cas de problème

    def __str__(self):
        return self.nom

    def nombre_emprunts_actifs(self):
        """Retourne le nombre d'emprunts en cours (non rendus)"""
        return self.emprunts.filter(date_retour__isnull=True).count()

    def a_un_retard(self):
        """Vérifie si le membre a au moins un emprunt en retard"""
        return self.emprunts.filter(date_retour__lt=timezone.now(), date_retour__isnull=False).exists()

    def peut_emprunter(self):
        """Un membre peut emprunter s'il a moins de 3 emprunts actifs et aucun retard"""
        return not self.bloque and not self.a_un_retard() and self.nombre_emprunts_actifs() < 3

# Modèle général pour les médias
class Media(models.Model):
    titre = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)  # Indique si le média est disponible ou emprunté

    def __str__(self):
        return self.titre

# Modèles spécifiques pour chaque média
class Livre(Media):
    auteur = models.CharField(max_length=100)

class DVD(Media):
    realisateur = models.CharField(max_length=100)

class CD(Media):
    artiste = models.CharField(max_length=100)

# Modèle pour les jeux de plateau (NON empruntables)
class JeuDePlateau(models.Model):
    nom = models.CharField(max_length=100)
    createur = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nom

# Modèle des emprunts
class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name="emprunts")
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField(default=date_retour_defaut)

    def save(self, *args, **kwargs):
        """Empêche l'emprunt de jeux de plateau et vérifie les conditions"""
        if isinstance(self.media, JeuDePlateau):
            raise ValueError("Les jeux de plateau ne peuvent pas être empruntés.")

        if not self.membre.peut_emprunter():
            raise ValueError("Ce membre a atteint la limite d'emprunts ou a un retard.")

        if not self.media.disponible:
            raise ValueError("Ce média est déjà emprunté.")

        # Marquer le média comme emprunté
        self.media.disponible = False
        self.media.save()
        super().save(*args, **kwargs)

    def est_en_retard(self):
        """Retourne True si l'emprunt est en retard"""
        return self.date_retour and timezone.now() > self.date_retour

    def rendre_media(self):
        """Marque l’emprunt comme terminé"""
        self.date_retour = timezone.now()
        self.media.disponible = True  # Remet le média comme disponible
        self.media.save()
        self.save()

    def __str__(self):
        return f"{self.media.titre} emprunté par {self.membre.nom} ({self.date_emprunt} - {self.date_retour})"
