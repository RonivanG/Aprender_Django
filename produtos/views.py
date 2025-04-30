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
        # Recebendo os dados do formulário
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        responsavel = request.POST.get('responsavel')
        telefone = request.POST.get('telefone')
        acao = request.POST.get('acao')  # Pega o valor do botão clicado

        # Ação de cadastro (Criar)
        if acao == "criar":
            # Verifica se já existe uma pessoa com o mesmo nome
            if NovaPessoa.objects.filter(nome=nome).exists():
                return HttpResponse("Usuário já cadastrado.")
            else:
                # Cria um novo objeto NovaPessoa
                pessoa = NovaPessoa(
                    nome=nome,
                    data_nascimento=data_nascimento,
                    rua=rua,
                    numero=numero,
                    bairro=bairro,
                    nome_responsavel=responsavel,
                    telefone=telefone
                )
                pessoa.save()  # Salva no banco de dados
                return HttpResponse("Usuário cadastrado com sucesso.")

        # Ação de pesquisa (Pesquisar)
        elif acao == "pesquisar":
            pessoas = NovaPessoa.objects.filter(nome=nome)  # Pesquisa pelo nome
            if pessoas.exists():
                # Se encontrar, envia os dados para o template para exibição
                return render(request, 'cadastro.html', {'pessoas': pessoas, 'nome': nome})
            else:
                return HttpResponse("Usuário não encontrado.")

        # Ação de deletar (Deletar)
        elif acao == "deletar":
            pessoas = NovaPessoa.objects.filter(nome=nome)  # Busca pelo nome
            if pessoas.exists():
                pessoas.delete()  # Deleta o usuário
                return HttpResponse("Usuário deletado com sucesso.")
            else:
                return HttpResponse("Usuário não encontrado para deletar.")

        else:
            return HttpResponse("Ação inválida.")
