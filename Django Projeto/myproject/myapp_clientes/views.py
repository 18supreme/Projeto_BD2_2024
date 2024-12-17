from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def clientes_home(request):
    user_id = request.session.get('user_id')
    with connection.cursor() as cursor:
            # Executar a consulta para contar o número total de reservas
            cursor.execute("""
                SELECT COUNT(id_reserva)
                FROM reserva
                WHERE id_utilizador = %s;
            """, [user_id]) 
            total_reservas = cursor.fetchone()[0]

            # Executar a consulta para obter a percentagem de danos para o usuário específico
            cursor.execute("""
                SELECT 
                    ROUND(
                        (SUM(CASE WHEN Danos = TRUE THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 
                        1
                    ) AS percentagem_com_danos
                FROM reserva
                WHERE id_utilizador = %s;
            """, [user_id])  # Substitua "userid" por %s e passe o valor de user_id
            percentagem_danos = cursor.fetchone()[0]

            # Executar a consulta para obter a marca mais usada
            cursor.execute("""
                SELECT marca.nome AS marca_preferida
                FROM reserva
                JOIN viatura ON reserva.id_viatura = viatura.id_viatura
                JOIN marca ON viatura.id_marca = marca.id_marca
                WHERE reserva.id_utilizador = %s  -- Filtro para o usuário específico
                GROUP BY marca.nome
                ORDER BY COUNT(*) DESC
                LIMIT 1;
            """, [user_id])  # Passa o ID_user para a consulta
            marca_preferida = cursor.fetchone()

            # Executar a consulta para obter o modelo mais usado
            cursor.execute("""
                SELECT modelo.nome AS modelo_preferido
                FROM reserva
                JOIN viatura ON reserva.id_viatura = viatura.id_viatura
                JOIN modelo ON viatura.id_modelo = modelo.id_modelo
                WHERE reserva.id_utilizador = %s  -- Filtro para o usuário específico
                GROUP BY modelo.nome
                ORDER BY COUNT(*) DESC
                LIMIT 1;
            """, [user_id])
            modelo_preferido = cursor.fetchone()

            # Executar a consulta para obter a média de KM realizados
            cursor.execute("""
                SELECT 
                    CONCAT(COALESCE(ROUND(SUM(KMPercorridos) * 1.0 / COUNT(KMPercorridos), 2), 0), ' KM') AS media_km
                FROM reserva
                WHERE reserva.id_utilizador = %s  -- Filtro para o usuário específico
            """, [user_id])
            MédiaKmPercorridos = cursor.fetchone()[0]  # Usando fetchall() para obter as 3 viaturas

            # Executar a consulta para obter a média de KM realizados
            cursor.execute("""
                SELECT 
                    CONCAT(COALESCE(SUM(KMPercorridos), 0), ' KM') AS total_km
                FROM reserva
                WHERE reserva.id_utilizador = %s  -- Filtro para o usuário específico
            """, [user_id])
            TotalKmPercorridos = cursor.fetchone()[0]  # Usando fetchall() para obter as 3 viaturas
            
        # Executar a consulta para obter as 3 viaturas mais requisitadas
            cursor.execute("""
                SELECT viatura.id_viatura, marca.nome AS marca, modelo.nome AS modelo, tipocaixa.nome AS caixa, COUNT(reserva.id_reserva) AS total_reservas
                FROM reserva
                JOIN viatura ON reserva.id_viatura = viatura.id_viatura
                JOIN marca ON viatura.id_marca = marca.id_marca
                JOIN modelo ON viatura.id_modelo = modelo.id_modelo
                JOIN tipocaixa ON tipocaixa.ID_Caixa = viatura.id_Tipocaixa
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
            SELECT vi.id_viatura, vi.matricula, mo.nome AS modelo, ma.nome AS marca, co.nome AS cor, i.Nome AS Combustivel, tc.Nome AS Tipo_Caixa, preco
            FROM viatura vi
            JOIN modelo mo ON vi.id_modelo = mo.id_modelo
            JOIN marca ma ON vi.id_marca = ma.id_marca
            JOIN cores co ON vi.id_cor = co.id_cor
            JOIN Combustivel i ON i.ID_Combustivel = vi.id_Combustivel
            JOIN TipoCaixa tc ON tc.ID_Caixa = vi.id_Tipocaixa
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
            JOIN Modelo mv ON mv.ID_Modelo = v.ID_Modelo
            JOIN Marca m ON m.ID_Marca = v.ID_Marca
            JOIN TipoViatura tv ON tv.ID_TipoViatura = v.ID_Tipo_Viatura
            JOIN Cores c ON c.ID_Cor = v.ID_Cor
            JOIN EstadoViatura ev ON ev.ID_EstadoViatura = v.ID_Estado_Viatura
            JOIN Combustivel i ON i.ID_Combustivel = v.ID_Combustivel
            JOIN TipoCaixa tc ON tc.ID_Caixa = v.ID_Tipocaixa
            JOIN Traccao tr ON tr.ID_Traccao = v.ID_Traccao
            WHERE v.ID_Viatura = %s
        """, [id])  # Passando o id como parâmetro de forma segura

        viatura = cursor.fetchone()  # Obtém uma linha de resultado

    if viatura:
        return render(request, 'viatura_detail.html', {'viatura': viatura})
    else:
        return render(request, 'viatura_detail.html', {'error': 'Viatura não encontrada.'})


def reservas_list(request):
    ID_user = request.session.get('user_id')
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
                estadoreserva ON reserva.ID_EstadoReserva = estadoreserva.ID_Estado_Reserva
            WHERE id_utilizador = %s
            ORDER BY 
                reserva.data_inicio DESC;
        """, [ID_user])
        reservas = cursor.fetchall()
    
    # Retorna a lista de viaturas para o template
    return render(request, 'reservas_list.html', {'reservas': reservas})


def criar_reserva(request, viatura_id):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        # Obtendo os valores do formulário
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

        # Verificando conflitos de reserva
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM Reserva
                WHERE ID_Viatura = %s
                AND (
                    (Data_Inicio <= %s AND Data_Fim >= %s)
                    OR (Data_Inicio <= %s AND Data_Fim >= %s)
                    OR (Data_Inicio >= %s AND Data_Inicio <= %s)
                )
                AND Reserva.id_estadoreserva != 5
            """, [viatura_id, data_inicio, data_fim, data_inicio, data_fim, data_inicio, data_fim])
            
            conflito = cursor.fetchone()[0]  # Obtem o primeiro resultado (contagem)

        if conflito > 0:
            # Se houver conflito, retorna uma mensagem ao usuário
            return HttpResponse("A viatura já está reservada nesse intervalo de datas.", status=400)

        # Se não houver conflito, insere a nova reserva
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Reserva (Data_Inicio, Data_Fim, Danos, DanosTexto, KMPercorridos, ID_Viatura, ID_Utilizador, ID_EstadoReserva)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [data_inicio, data_fim, False, '', 0, viatura_id, user_id , 1])

        # Redireciona para a lista de viaturas
        return redirect('viaturas_list')

    # Se for uma requisição GET, exibe o formulário
    return render(request, 'reserva_form.html')


def reserva_cancelar(request, reserva_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Atualiza o estado da reserva para o estado com id=5
            cursor.execute("""
                UPDATE Reserva
                SET ID_EstadoReserva = 5
                WHERE id_reserva = %s
            """, [reserva_id])  # Usando o parametro id_reserva de forma segura

            # Adicionar mensagem de sucesso
        return redirect('reservas_list')

    # Se for uma requisição GET, exibe o formulário
    return render(request, 'reservas_list.html')
