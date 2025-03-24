
# Gestion-de-Mediatheque

Description
Ce projet est une application Django permettant de moderniser la gestion d'une médiathèque. Il offre deux interfaces : une pour les bibliothécaires (gestion des membres, emprunts, médias...) et une pour les membres (consultation des médias).

# Fonctionnalités

Application Bibliothécaire:

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

static/ : fichiers statiques (CSS, images...)

db.sqlite3 : base de données locale

# Contraintes:

- Un membre ne peut pas avoir plus de 3 emprunts à la fois.
- Un membre ayant un emprunt en retard ne peut pas emprunter.
- Un emprunt est limité à 7 jours.
- Les jeux de plateau ne sont pas empruntables.


