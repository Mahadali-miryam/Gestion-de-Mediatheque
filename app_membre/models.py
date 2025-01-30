
from django.db import models

class Membre(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.nom
