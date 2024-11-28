from django.shortcuts import render
from django.db import connection

def clientes_home(request):
    with connection.cursor() as cursor:
        # Executar a consulta para contar o número total de reservas
        cursor.execute("""
            SELECT COUNT(id_reserva)
            FROM reserva;
        """)
        total_reservas = cursor.fetchone()[0]

        # Executar a consulta para obter a marca mais usada
        cursor.execute("""
            SELECT marca.nome AS marca_preferida
            FROM reserva
            JOIN viatura ON reserva.id_viatura = viatura.id_viatura
            JOIN marca ON viatura.id_marca = marca.id_marca
            GROUP BY marca.nome
            ORDER BY COUNT(*) DESC
            LIMIT 1;
        """)
        marca_preferida = cursor.fetchone()

        # Executar a consulta para obter o modelo mais usado
        cursor.execute("""
            SELECT modelo.nome AS modelo_preferido
            FROM reserva
            JOIN viatura ON reserva.id_viatura = viatura.id_viatura
            JOIN modelo ON viatura.id_modelo = modelo.id_modelo
            GROUP BY modelo.nome
            ORDER BY COUNT(*) DESC
            LIMIT 1;
        """)
        modelo_preferido = cursor.fetchone()

        # Executar a consulta para obter as 3 viaturas mais requisitadas
        cursor.execute("""
            SELECT viatura.id_viatura, marca.nome AS marca, modelo.nome AS modelo, COUNT(reserva.id_reserva) AS total_reservas
            FROM reserva
            JOIN viatura ON reserva.id_viatura = viatura.id_viatura
            JOIN marca ON viatura.id_marca = marca.id_marca
            JOIN modelo ON viatura.id_modelo = modelo.id_modelo
            GROUP BY viatura.id_viatura, viatura.id_modelo, marca.nome, modelo.nome
            ORDER BY total_reservas DESC
            LIMIT 3;
        """)
        viaturas_tendencias = cursor.fetchall()  # Usando fetchall() para obter as 3 viaturas

    # Passar os valores para o template
    return render(request, 'clientes_home.html', {
        'total_reservas': total_reservas,
        'marca_preferida': marca_preferida[0] if marca_preferida else "Nenhuma marca encontrada",
        'modelo_preferido': modelo_preferido[0] if modelo_preferido else "Nenhum modelo encontrado",
        'viaturas': viaturas_tendencias  # Passando a lista de viaturas
    })

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
    
def reservas_list(request):
    # Executa a consulta SQL direta para obter as viaturas
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                reserva.id_reserva AS id,
                marca.nome AS marca, 
                modelo.nome AS modelo, 
                estadoreserva.estado AS status, 
                reserva.data_inicio AS data_inicio, 
                reserva.data_fim AS data_fim,
                reserva.danos AS danos
            FROM 
                reserva
            JOIN 
                viatura ON viatura.id_viatura = reserva.id_viatura
            JOIN 
                marca ON viatura.id_marca = marca.id_marca
            JOIN 
                modelo ON viatura.id_modelo = modelo.id_modelo
            JOIN 
                estadoreserva ON reserva.estado_reserva = estadoreserva.id_estado_reserva
            ORDER BY 
                reserva.data_inicio DESC;
        """)
        reservas = cursor.fetchall()
    
    # Retorna a lista de viaturas para o template
    return render(request, 'reservas_list.html', {'reservas': reservas})