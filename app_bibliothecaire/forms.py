from django import forms
from .models import Membre
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Entrez votre nom d'utilisateur"}))
    password = forms.CharField(label="Mot de passe", max_length=30, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': "Entrez votre mot de passe"}))


class Creationmembre(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du membre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
