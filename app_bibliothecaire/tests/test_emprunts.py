from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from app_bibliothecaire.models import Membre, Livre, Emprunt

class EmpruntTestCase(TestCase):
    def setUp(self):
        """Créer un membre et un livre disponible pour les tests"""
        self.membre = Membre.objects.create(nom="Test Membre", email="test@example.com")
        self.livre = Livre.objects.create(titre="Livre Test", auteur="Auteur Test", disponible=True)  # ✅ Vérifie bien True ici !

    def test_emprunt_livre(self):
        """Tester qu'un membre peut emprunter un livre"""
        emprunt = Emprunt.objects.create(
            membre=self.membre,
            media_type="livre",
            media_id=self.livre.id,
            date_emprunt=timezone.now(),
            date_retour=timezone.now() + timedelta(days=7)
        )

        # 🔹 Mettre à jour le livre après l'emprunt
        self.livre.refresh_from_db()  # 🔄 Force la mise à jour

        # 🔥 TEST : Vérifier que le livre est maintenant indisponible
        self.assertFalse(self.livre.disponible, "Le livre devrait être marqué comme non disponible après l'emprunt.")

