
# Gestion-de-Mediatheque

# Description
Ce projet est une application Django permettant de moderniser la gestion d'une médiathèque. Il offre deux interfaces : une pour les bibliothécaires (gestion des membres, emprunts, médias...) et une pour les membres (consultation des médias).

# Fonctionnalités

1 Application Bibliothécaire:

 - Créer, modifier et supprimer des membres.
 - Ajouter, modifier et supprimer des médias :
 - Livres
 - CDs
 - DVDs
 - Jeux de plateau (consultation uniquement, pas d’emprunt).
 - Gérer les emprunts et les retours de médias.
 - Afficher la liste des emprunts en cours ou en retard.

Application Membre:

Consulter la liste des médias disponibles.

# Installation

## Exécution du projet
Cloner le dépôt :
git clone https://github.com/Mahadali-miryam/Gestion-de-Mediatheque.git

cd Gestion-de-Mediatheque

 Créer et activer un environnement virtuel :

. python -m venv venv

. venv\Scripts\activate

. pip install -r requirements.txt

 Configurer la base de données :

. python manage.py makemigrations
. python manage.py migrate
. Charger des données de test (fixtures) :
. python manage.py loaddata app_bibliothecaire/fixtures/membres.json

 Créer un superutilisateur : python manage.py createsuperuser

Lancer le serveur de développement : python manage.py runserver

L'application sera accessible à l'adresse : http://127.0.0.1:8000/

# Tests
Pour exécuter les tests unitaires : python manage.py test

# Structure du projet

app_bibliothecaire/ : application principale (bibliothécaires)

templates/ : fichiers HTML

fixtures/ : données de test

static/ : fichiers statiques (images...)

app_membre/ : application pour les membres (consultation)

db.sqlite3 : base de données locale

# Contraintes:

- Un membre ne peut pas avoir plus de 3 emprunts à la fois.
- Un membre ayant un emprunt en retard ne peut pas emprunter.
- Un emprunt est limité à 7 jours.
- Les jeux de plateau ne sont pas empruntables.

#  Rapport du Projet
# Étude et correctifs du code fourni
Le code initial commencé par le developpeur était très basique et présentait plusieurs défauts importants que j'ai rapidement identifiés :

Les modèles n’étaient pas bien structurés et les contraintes métier essentielles n’étaient pas intégrées.

La gestion des emprunts était absente, ainsi que la différenciation entre les types de médias.

La séparation entre l’application des bibliothécaires et celle des membres n’était pas claire.

# Ce que j’ai corrigé :

Création claire et structurée des modèles Django (Livre, DVD, CD, JeuDePlateau, Emprunt, Membre).

Application stricte des contraintes métier : limite de 3 emprunts maximum par membre, obligation de retour après 7 jours, blocage de nouveaux emprunts en cas de retard.

Séparation explicite des applications : app_bibliothecaire (gestion complète des médias et des membres) et app_membre (consultation uniquement).

 # Mise en place des fonctionnalités demandées
Application Bibliothécaire :

Gestion complète des membres : ajouter, modifier et supprimer facilement.

Gestion complète des médias : ajout, modification et suppression des livres, CDs, DVDs et jeux de plateau.

Gestion des emprunts avec création, retour des médias et affichage clair des emprunts en cours, tout en respectant automatiquement les règles métier définies.

Application Membre :

Consultation facile et claire de la liste complète des médias disponibles.

# Stratégie de tests
J’ai mis en place des tests unitaires afin de garantir que chaque fonctionnalité importante fonctionne correctement :

Utilisation des classes TestCase de Django pour tester en détail les modèles et les vues.

Tests précis réalisés pour valider :

Le bon fonctionnement de la gestion des emprunts.

Le respect des limites imposées (nombre maximum d'emprunts, durée d'emprunt).

La gestion des médias déjà empruntés.

Ces tests automatiques assurent une stabilité et une fiabilité à mon application.

#  Base de données avec données test
J’ai choisi SQLite pour la simplicité d’utilisation et d’installation rapide. J’ai intégré des données de test via des fixtures au format JSON (fixtures.json) :

Membres fictifs comme Megane SIGNES ou Maeva AVA.

Médias fictifs pour illustrer différents cas d'utilisation comme "Le Seigneur des Anneaux", "Harry Potter", "1984".

Emprunts fictifs montrant les cas normaux et les cas limites du projet.

