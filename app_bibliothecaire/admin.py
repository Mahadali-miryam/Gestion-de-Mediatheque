from django.contrib import admin
from .models import Livre, DVD, CD, Membre, JeuDePlateau

# Register your models here.

admin.site.register(Livre)
admin.site.register(DVD)
admin.site.register(CD)
admin.site.register(Membre)
admin.site.register(JeuDePlateau)
