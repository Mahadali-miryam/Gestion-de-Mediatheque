from django.contrib import admin
from .models import Emprunt, Livre, DVD, CD, Membre, JeuDePlateau

# Register your models here.
admin.site.register(Emprunt)
admin.site.register(Livre)
admin.site.register(DVD)
admin.site.register(CD)
admin.site.register(Membre)
admin.site.register(JeuDePlateau)
