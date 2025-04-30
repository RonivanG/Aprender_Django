from django.shortcuts import render
from django.http import HttpResponse
from .models import NovaPessoa

def minha_pagina(request):
    return render(request, 'index.html')

def sobre_projeto(request):
    return render(request, 'sobre.html')

def login(request):
    return render(request, 'login.html')

def cadastro_crianca(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')

    elif request.method == "POST":
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        acao = request.POST.get('acao')  # pega o valor do botão clicado

        if acao == "criar":
            if NovaPessoa.objects.filter(nome=nome).exists():
                return HttpResponse("Usuário já cadastrado.")
            else:
                pessoa = NovaPessoa(nome=nome, idade=idade)
                pessoa.save()
                return HttpResponse("Usuário cadastrado com sucesso.")

        elif acao == "deletar":
            pessoas = NovaPessoa.objects.filter(nome=nome)
            if pessoas.exists():
                pessoas.delete()
                return HttpResponse("Usuário deletado com sucesso.")
            else:
                return HttpResponse("Usuário não encontrado para deletar.")

        elif acao == "pesquisar":
            pessoas = NovaPessoa.objects.filter(nome=nome)
            if pessoas.exists():
                return render(request, 'cadastro.html', {'pessoas': pessoas, 'nome': nome})
            else:
                return HttpResponse("Usuário não encontrado.")

        else:
            return HttpResponse("Ação inválida.")

