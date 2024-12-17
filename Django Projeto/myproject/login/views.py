from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate, login
from . import basededados as bd

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = bd.getUserByUsernameAndPassword(username, password)
        
        if user:
            ID_user, username, tipo_utilizador = user  # Desempacota os resultados
            
            # Armazena o ID do usuário na sessão
            request.session['ID_user'] = ID_user  # Armazenar o ID, não o nome
            
            # Exemplo de redirecionamento com base no tipo de utilizador
            if tipo_utilizador == 'Cliente':
                return redirect('clientes_home')
            elif tipo_utilizador == 'Admin':
                return redirect('admin_home')
        else:
            # Caso as credenciais sejam inválidas
            return render(request, 'login.html', {'error': 'Credenciais inválidas.'})
    
    return render(request, 'login.html')

def logout(request):
    # Limpa a sessão e realiza o logout do usuário
    if 'ID_user' in request.session:
        del request.session['ID_user']  # Remove o ID do usuário da sessão
    
    django_logout(request)  # Logout do Django, limpa a sessão
    return redirect('login')  # Redireciona para a página de login