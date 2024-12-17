from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, redirect


def admin_home(request):
    user_id = request.session.get('ID_user')

    return render(request, 'admin_home.html')


def admin_viaturas(request):
    return render(request, 'admin_viaturas.html')


def admin_reservas(request):
    return render(request, 'admin_reservas.html')


def admin_manutencoes(request):
    return render(request, 'admin_manutencoes.html')


def admin_administracao(request):
    return render(request, 'admin_administracao.html')

def admin_marcaslist(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM marca
        """)
        marcas = cursor.fetchall()
    
    # Retorna a lista de viaturas para o template
    return render(request, 'admin_marcaslist.html', {'marcas': marcas})

def admin_marcadelete(request, marcaid):
    with connection.cursor() as cursor:
        cursor.execute("""
                DELETE FROM marca where id_marca = %s
            """, [marcaid])
        
    return redirect('admin_marcaslist')