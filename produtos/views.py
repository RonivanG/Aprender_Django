from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import NovaPessoa
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def minha_pagina(request):
    return render(request, 'index.html')

def contato_projeto(request):
    return render(request, 'contato.html')

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
        crianca_id = request.GET.get('id')
        crianca = None
        if crianca_id:
            crianca = get_object_or_404(NovaPessoa, id=crianca_id)
        return render(request, 'cadastro.html', {'crianca': crianca})

    elif request.method == "POST":
        acao = request.POST.get('acao')

        if acao == "criar":
            nome = request.POST.get('nome')
            data_nascimento = request.POST.get('data_nascimento')
            rua = request.POST.get('rua')
            numero = request.POST.get('numero')
            bairro = request.POST.get('bairro')
            responsavel = request.POST.get('responsavel')
            telefone = request.POST.get('telefone')

            pessoa = NovaPessoa(
                nome=nome,
                data_nascimento=data_nascimento,
                rua=rua,
                numero=numero,
                bairro=bairro,
                nome_responsavel=responsavel,
                telefone=telefone
            )
            pessoa.save()
            return HttpResponse("Criança cadastrada com sucesso.")

        else:
            return HttpResponse("Ação inválida.")

@login_required
def atualizar_crianca(request):
    if request.method == "GET":
        crianca_id = request.GET.get('id')
        crianca = None
        if crianca_id:
            crianca = get_object_or_404(NovaPessoa, id=crianca_id)
        return render(request, 'atualizar.html', {'crianca': crianca})

    elif request.method == "POST":
        acao = request.POST.get('acao')

        if acao == "deletar":
            crianca_id_deletar = request.POST.get('id_deletar')
            if crianca_id_deletar:
                try:
                    crianca = NovaPessoa.objects.get(id=crianca_id_deletar)
                    crianca.delete()
                    return HttpResponse("Criança deletada com sucesso.")
                except NovaPessoa.DoesNotExist:
                    return HttpResponse("Criança não encontrada para deletar.")
            else:
                return HttpResponse("ID da criança para deletar não fornecido.")

        elif acao == "editar":
            crianca_id_editar = request.POST.get('id_editar')
            if crianca_id_editar:
                try:
                    crianca = NovaPessoa.objects.get(id=crianca_id_editar)
                    crianca.nome = request.POST.get('nome')
                    crianca.data_nascimento = request.POST.get('data_nascimento')
                    crianca.rua = request.POST.get('rua')
                    crianca.numero = request.POST.get('numero')
                    crianca.bairro = request.POST.get('bairro')
                    crianca.nome_responsavel = request.POST.get('responsavel')
                    crianca.telefone = request.POST.get('telefone')
                    crianca.save()
                    return HttpResponse("Dados da criança atualizados com sucesso.")
                except NovaPessoa.DoesNotExist:
                    return HttpResponse("Criança não encontrada para editar.")
            else:
                return HttpResponse("ID da criança para editar não fornecido.")

        else:
            return HttpResponse("Ação inválida.")
        
@login_required
def pesquisa_crianca(request):
    nome_param = request.GET.get('nome')
    responsavel_param = request.GET.get('nome_responsavel')
    resultados = []

    if nome_param:
        if responsavel_param:
            # Pesquisa por nome E responsável
            resultados = NovaPessoa.objects.filter(
                Q(nome__icontains=nome_param) & Q(nome_responsavel__icontains=responsavel_param)
            )
        else:
            # Pesquisa apenas por nome
            resultados = NovaPessoa.objects.filter(nome__icontains=nome_param)
    else:
        # Se nenhum nome foi fornecido (o campo é obrigatório no HTML,
        # mas é bom ter uma verificação no backend também)
        mensagem_erro = "O nome da criança é obrigatório para a pesquisa."
        return render(request, 'pesquisa.html', {'mensagem_erro': mensagem_erro})

    context = {'resultados': resultados}
    return render(request, 'pesquisa.html', context)

