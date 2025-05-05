from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_crianca/', views.cadastro_crianca, name='cadastro_crianca'),
    path('sobre_projeto/', views.sobre_projeto, name='sobre_projeto'),
    path('login/', views.login, name='login'),
    path('resetar_senha/', views.resetar_senha, name='resetar_senha'),
]