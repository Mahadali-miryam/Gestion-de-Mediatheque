from django.urls import path
from . import views

urlpatterns = [
    # Exemple de route
    path('liste/', views.liste_membres, name='liste_membres'),
]