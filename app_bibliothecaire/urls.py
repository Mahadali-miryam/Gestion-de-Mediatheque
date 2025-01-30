from django.urls import path
from .views import liste_membres, ajout_membre, supprimer_membre, liste_medias, ajouter_media, supprimer_media, \
    liste_emprunts, emprunter_media, retourner_media

urlpatterns = [
    path('membres/', liste_membres, name='liste_membres'),
    path('membres/ajout/', ajout_membre, name='ajout_membre'),
    path('membres/supprimer/<int:membre_id>/', supprimer_membre, name='supprimer_membre'),

    path('medias/', liste_medias, name='liste_medias'),
    path('medias/ajouter/<str:media_type>/', ajouter_media, name='ajouter_media'),
    path('medias/supprimer/<int:media_id>/<str:media_type>/', supprimer_media, name='supprimer_media'),

    path('emprunts/', liste_emprunts, name='liste_emprunts'),
    path('emprunter/<str:media_type>/<int:media_id>/', emprunter_media, name='emprunter_media'),
    path('retourner/<int:emprunt_id>/', retourner_media, name='retourner_media'),
]
