from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('app_bibliothecaire.urls')),
    # path('emprunteur/', include('app_membre.urls')),
    path('membre/', include('app_membre.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]


