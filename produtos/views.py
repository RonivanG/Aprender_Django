from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import NovaPessoa
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class ResetSenhaForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nome de Usuário')
    new_password = forms.CharField(widget=forms.PasswordInput, label='Nova Senha')
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Nova Senha')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        new_password = self.cleaned_data['new_password']
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return True
        except User.DoesNotExist:
            self.add_error('username', 'Usuário não encontrado.')
            return False

def minha_pagina(request):
    return render(request, 'index.html')

def sobre_projeto(request):
    return render(request, 'sobre.html')


def logout(request):
    auth_logout(request)  # Encerra a sessão do usuário
    return redirect('/')  # Redireciona para a página inicial (ou outra página desejada)

def login(request):
    if request.method == 'POST':
        # Obtém o username e password do formulário enviado via POST
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentica o usuário com as credenciais fornecidas
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Se o usuário for autenticado com sucesso, faz o login
            auth_login(request, user)
            # Redireciona para a página inicial (ajuste a URL conforme necessário)
            return redirect('/') # Ou para outra URL como 'home'
        else:
            # Se a autenticação falhar, exibe uma mensagem de erro (opcional)
            messages.error(request, 'Usuário ou senha inválidos.')
            # Renderiza a página de login novamente
            return render(request, 'login.html')
    else:
        # Se a requisição for GET, apenas renderiza a página de login
        return render(request, 'login.html')
    
def resetar_senha(request):
    if request.method == 'POST':
        form = ResetSenhaForm(request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('login')  # Redirecione para a página de login após o sucesso
            else:
                messages.error(request, 'Erro ao alterar a senha. Verifique o nome de usuário.')
    else:
        form = ResetSenhaForm()
    return render(request, 'reset_senha.html', {'form': form})
@login_required
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
