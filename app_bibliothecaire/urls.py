from django.urls import path
from . import views

urlpatterns = [
    # 🔐 Authentification
    path('', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # 👥 Gestion des membres
    path('membres/', views.liste_membres, name='liste_membres'),
    path('ajout-membre/', views.ajout_membre, name='ajout_membre'),
    path('modifier-membre/<int:membre_id>/', views.modifier_membre, name='modifier_membre'),
    path('supprimer-membre/<int:membre_id>/', views.supprimer_membre, name='supprimer_membre'),

    # 📚 Gestion des médias
    path('medias/', views.liste_medias, name='liste_medias'),
    path('ajouter-livre/', views.ajouter_livre, name='ajouter_livre'),
    path('ajouter-dvd/', views.ajouter_dvd, name='ajouter_dvd'),
    path('ajouter-cd/', views.ajouter_cd, name='ajouter_cd'),
    path('ajouter-jeu-de-plateau/', views.ajouter_jeu_de_plateau, name='ajouter_jeu_de_plateau'),

    # 📖 Gestion des emprunts
    path('emprunter/<str:media_type>/<int:media_id>/', views.emprunter_media, name='emprunter_media'),
    path('retourner/<int:emprunt_id>/', views.retourner_media, name='retourner_media'),
    path('emprunts/', views.liste_emprunts, name='liste_emprunts'),


    # 🗑 Suppression des médias (Ajoute ces lignes si elles manquent)
    path('supprimer-livre/<int:livre_id>/', views.supprimer_livre, name='supprimer_livre'),
    path('supprimer-dvd/<int:dvd_id>/', views.supprimer_dvd, name='supprimer_dvd'),
    path('supprimer-cd/<int:cd_id>/', views.supprimer_cd, name='supprimer_cd'),

    # ℹ️ Pages d'information
    path('confirmation-emprunt/', views.confirmation_emprunt, name='confirmation_emprunt'),
    path('limite-emprunts/', views.limite_emprunts, name='limite_emprunts'),
    path('emprunts-en-retard/', views.emprunts_en_retard, name='emprunts_en_retard'),
]
