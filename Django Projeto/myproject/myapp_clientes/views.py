from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse

def clientes_home(request):
    with connection.cursor() as cursor:
        # Executar a consulta para contar o número total de reservas
        cursor.execute("""
            SELECT COUNT(id_reserva)
            FROM reserva;
        """)
        total_reservas = cursor.fetchone()[0]

        cursor.execute("""
            SELECT 
                ROUND(
                    (SUM(CASE WHEN Danos = TRUE THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 
                    1
                ) AS percentagem_com_danos
            FROM reserva;
        """)
        percentagem_danos = cursor.fetchone()[0]

        # Executar a consulta para obter a marca mais usada
        cursor.execute("""
            SELECT marca.nome AS marca_preferida
            FROM reserva
            JOIN viatura ON reserva.viatura_id = viatura.id_viatura
            JOIN marca ON viatura.marca_id = marca.id_marca
            GROUP BY marca.nome
            ORDER BY COUNT(*) DESC
            LIMIT 1;
        """)
        marca_preferida = cursor.fetchone()

        # Executar a consulta para obter o modelo mais usado
        cursor.execute("""
            SELECT modelo.nome AS modelo_preferido
            FROM reserva
            JOIN viatura ON reserva.viatura_id = viatura.id_viatura
            JOIN modelo ON viatura.modelo_id = modelo.id_modelo
            GROUP BY modelo.nome
            ORDER BY COUNT(*) DESC
            LIMIT 1;
        """)
        modelo_preferido = cursor.fetchone()

        # Executar a consulta para obter a média de KM realizados
        cursor.execute("""
            SELECT 
                CONCAT(COALESCE(ROUND(SUM(KMPercorridos) * 1.0 / COUNT(KMPercorridos), 2), 0), ' KM') AS media_km
            FROM reserva;
        """)
        MédiaKmPercorridos = cursor.fetchone()[0]  # Usando fetchall() para obter as 3 viaturas

        # Executar a consulta para obter a média de KM realizados
        cursor.execute("""
            SELECT 
                CONCAT(COALESCE(SUM(KMPercorridos), 0), ' KM') AS total_km
            FROM reserva;
        """)
        TotalKmPercorridos = cursor.fetchone()[0]  # Usando fetchall() para obter as 3 viaturas
        
        # Executar a consulta para obter as 3 viaturas mais requisitadas
        cursor.execute("""
            SELECT viatura.id_viatura, marca.nome AS marca, modelo.nome AS modelo, tipocaixa.nome AS caixa, COUNT(reserva.id_reserva) AS total_reservas
            FROM reserva
            JOIN viatura ON reserva.viatura_id = viatura.id_viatura
            JOIN marca ON viatura.marca_id = marca.id_marca
            JOIN modelo ON viatura.modelo_id = modelo.id_modelo
            JOIN tipocaixa ON tipocaixa.ID_Caixa = viatura.Tipocaixa_ID
            GROUP BY viatura.id_viatura, modelo.nome, tipocaixa.nome, marca.nome, modelo.nome
                       
            ORDER BY total_reservas DESC
            LIMIT 3;
        """)
        viaturas_tendencias = cursor.fetchall()  # Usando fetchall() para obter as 3 viaturas

    # Passar os valores para o template
    return render(request, 'clientes_home.html', {
        'total_reservas': total_reservas if total_reservas else "Sem reservas",
        'percentagem_danos': percentagem_danos if percentagem_danos else "0",
        'marca_preferida': marca_preferida[0] if marca_preferida else "-",
        'modelo_preferido': modelo_preferido[0] if modelo_preferido else "-",
        'mediaKmPercorridos': MédiaKmPercorridos if MédiaKmPercorridos else "0",
        'TotalKmPercorridos': TotalKmPercorridos if TotalKmPercorridos else "0",
        'viaturas': viaturas_tendencias  # Passando a lista de viaturas
    })

def viaturas_list(request):
    # Executa a consulta SQL direta para obter as viaturas
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT vi.id_viatura, vi.matricula, mo.nome AS modelo, ma.nome AS marca, co.nome AS cor
            FROM viatura vi
            JOIN modelo mo ON vi.modelo_id = mo.id_modelo
            JOIN marca ma ON vi.marca_id = ma.id_marca
            JOIN cores co ON vi.cor_id = co.id_cor
        """)
        viaturas = cursor.fetchall()
    
    # Retorna a lista de viaturas para o template
    return render(request, 'viaturas_list.html', {'viaturas': viaturas})

def viatura_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                v.ID_Viatura, v.Matricula, v.KM, v.Ano, 
                mv.Nome AS Modelo, 
                m.Nome AS Marca, 
                tv.Nome AS Tipo_Viatura, 
                c.Nome AS Cor, 
                ev.Estado AS Estado_Viatura, 
                i.Nome AS Combustivel, 
                tc.Nome AS Tipo_Caixa, 
                tr.Nome AS Traccao
            FROM Viatura v
            JOIN Modelo mv ON mv.ID_Modelo = v.Modelo_ID
            JOIN Marca m ON m.ID_Marca = v.Marca_ID
            JOIN TipoViatura tv ON tv.ID_TipoViatura = v.Tipo_Viatura_ID
            JOIN Cores c ON c.ID_Cor = v.Cor_ID
            JOIN EstadoViatura ev ON ev.ID_EstadoViatura = v.Estado_Viatura_ID
            JOIN Combustivel i ON i.ID_Combustivel = v.Combustivel_ID
            JOIN TipoCaixa tc ON tc.ID_Caixa = v.Tipocaixa_ID
            JOIN Traccao tr ON tr.ID_Traccao = v.Traccao_ID
            WHERE v.ID_Viatura = %s
        """, [id])  # Passando o id como parâmetro de forma segura

        viatura = cursor.fetchone()  # Obtém uma linha de resultado

    if viatura:
        return render(request, 'viatura_detail.html', {'viatura': viatura})
    else:
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
                viatura ON viatura.id_viatura = reserva.viatura_id
            JOIN 
                marca ON viatura.marca_id = marca.id_marca
            JOIN 
                modelo ON viatura.modelo_id = modelo.id_modelo
            JOIN 
                estadoreserva ON reserva.EstadoReserva_ID = estadoreserva.ID_Estado_Reserva
            ORDER BY 
                reserva.data_inicio DESC;
        """)
        reservas = cursor.fetchall()
    
    # Retorna a lista de viaturas para o template
    return render(request, 'reservas_list.html', {'reservas': reservas})

def criar_reserva(request, viatura_id):
    if request.method == 'POST':
        # Obtendo os valores do formulário
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

        # Verificando conflitos de reserva
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM Reserva
                WHERE Viatura_ID = %s
                AND (
                    (Data_Inicio <= %s AND Data_Fim >= %s)
                    OR (Data_Inicio <= %s AND Data_Fim >= %s)
                    OR (Data_Inicio >= %s AND Data_Inicio <= %s)
                )
            """, [viatura_id, data_inicio, data_fim, data_inicio, data_fim, data_inicio, data_fim])
            
            conflito = cursor.fetchone()[0]  # Obtem o primeiro resultado (contagem)

        if conflito > 0:
            # Se houver conflito, retorna uma mensagem ao usuário
            return HttpResponse("A viatura já está reservada nesse intervalo de datas.", status=400)

        # Se não houver conflito, insere a nova reserva
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Reserva (Data_Inicio, Data_Fim, Danos, DanosTexto, KMPercorridos, Viatura_ID, Utilizador_ID, EstadoReserva_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [data_inicio, data_fim, False, '', 0, viatura_id, 1, 1])

        # Redireciona para a lista de viaturas
        return redirect('viaturas_list')

    # Se for uma requisição GET, exibe o formulário
    return render(request, 'reserva_form.html')
