from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate, login

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Executar o JOIN para obter o tipo de utilizador
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.id_utilizador, u.nome, tu.tipo
                FROM utilizador u
                JOIN tipoutilizador tu ON u.id_tipoutilizador = tu.id_tipoutilizador
                WHERE u.nome = %s AND u.password = %s
            """, [username, password])
            
            user = cursor.fetchone()  # Retorna um único registro (ou None)
        
        if user:
            ID_user, username, tipo_utilizador = user  # Desempacota os resultados
            
            # Armazena o ID do usuário na sessão
            request.session['user_id'] = ID_user  # Armazenar o ID, não o nome
            print(tipo_utilizador)
            # Exemplo de redirecionamento com base no tipo de utilizador
            if tipo_utilizador == 'Cliente':
                return redirect('clientes_home')
            elif tipo_utilizador == 'Admin':
                return redirect('admin_home')

        else:
            # Caso as credenciais sejam inválidas
            print("Credenciais inválidas")
            return render(request, 'login.html', {'error': 'Credenciais inválidas.'})
    
    return render(request, 'login.html')

def logout(request):
    # Limpa a sessão e realiza o logout do usuário
    if 'ID_user' in request.session:
        del request.session['ID_user']  # Remove o ID do usuário da sessão
    
    django_logout(request)  # Logout do Django, limpa a sessão
    return redirect('login')  # Redireciona para a página de login