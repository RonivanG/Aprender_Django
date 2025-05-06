from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_crianca/', views.cadastro_crianca, name='cadastro_crianca'),
    path('pesquisa_crianca/', views.pesquisa_crianca, name='pesquisa_crianca'),
    path('contato_projeto/', views.contato_projeto, name='contato_projeto'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('resetar_senha/', views.resetar_senha, name='resetar_senha'),
]