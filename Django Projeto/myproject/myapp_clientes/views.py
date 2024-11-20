from django.shortcuts import render
from django.db import connection

def clientes_home(request):
    return render(request, 'clientes_home.html')

def viaturas_list(request):
    # Executa a consulta SQL direta para obter as viaturas
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT vi.id_viatura, vi.matricula, mo.nome AS modelo, ma.nome AS marca, co.nome AS cor
            FROM viatura vi
            JOIN modelo mo ON vi.id_modelo = mo.id_modelo
            JOIN marca ma ON vi.id_marca = ma.id_marca
            JOIN cores co ON vi.id_cor = co.id_cor
        """)
        viaturas = cursor.fetchall()
    
    # Retorna a lista de viaturas para o template
    return render(request, 'viaturas_list.html', {'viaturas': viaturas})

def viatura_detail(request, id):
    # Usar a conexão do Django para executar a consulta SQL
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT v.ID_Viatura, v.Matricula, v.KM, v.Ano, 
                   mv.Nome AS Modelo, m.Nome AS Marca, 
                   tv.Nome AS Tipo_Viatura, c.Nome AS Cor, 
                   ev.Estado
            FROM Viatura v
            JOIN Modelo mv ON mv.ID_Modelo = v.ID_Modelo
            JOIN Marca m ON m.ID_Marca = v.ID_Marca
            JOIN TipoViatura tv ON tv.ID_Tipo_Viatura = v.ID_Tipo_Viatura
            JOIN Cores c ON c.ID_Cor = v.ID_Cor
            JOIN EstadoViatura ev ON ev.ID_Estado_Viatura = v.ID_Estado_Viatura
            WHERE v.ID_Viatura = %s
        """, [id])

        # Recuperar o resultado da consulta
        viatura = cursor.fetchone()  # fetchone() para pegar um único registro

    if viatura:
        # Passar os dados da viatura para o template
        return render(request, 'viatura_detail.html', {'viatura': viatura})
    else:
        # Caso não exista a viatura, redirecionar ou exibir uma mensagem de erro
        return render(request, 'viatura_detail.html', {'error': 'Viatura não encontrada.'})