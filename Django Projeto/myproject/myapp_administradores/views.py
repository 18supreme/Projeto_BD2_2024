from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, redirect
from . import basededados as bd


def admin_home(request):
    user_id = request.session.get('ID_user')

    with connection.cursor() as cursor:
        # Contar o total de viaturas
        cursor.execute("SELECT COUNT(*) FROM viatura")
        total_viaturas = cursor.fetchone()[0]

        # Contar o total de reservas
        cursor.execute("SELECT COUNT(*) FROM reserva")
        total_reservas = cursor.fetchone()[0]

        # Contar manutenções pendentes
        cursor.execute("SELECT COUNT(*) FROM manutencao")
        manutencoes_pendentes = cursor.fetchone()[0]

        # Contar o total de veículos com danos
        cursor.execute("SELECT COUNT(*) FROM reserva WHERE danos = true")
        total_danos = cursor.fetchone()[0]

        # Contar o total de peças em stock
        cursor.execute("SELECT SUM(stock) FROM pecas")
        total_pecas = cursor.fetchone()[0]

        # Contar o total de viaturas disponíveis para reserva
        cursor.execute("SELECT COUNT(*) FROM viatura WHERE id_estado_viatura = 1")
        total_viaturas_reserva = cursor.fetchone()[0]

        # Buscar as 5 reservas mais recentes
        cursor.execute("""
            SELECT 
                r.id_reserva,
                r.data_inicio,
                r.data_fim,
                r.danos,
                r.danostexto,
                r.kmpercorridos,
                CONCAT(marca.nome, ' ', modelo.nome) AS nome_viatura,
                utilizador.nome AS nome_utilizador,
                estadoreserva.estado
            FROM reserva r
            LEFT JOIN viatura v ON r.id_viatura = v.id_viatura
            LEFT JOIN marca ON v.id_marca = marca.id_marca
            LEFT JOIN modelo ON v.id_modelo = modelo.id_modelo
            LEFT JOIN utilizador ON r.id_utilizador = utilizador.id_utilizador
            LEFT JOIN estadoreserva ON r.id_estadoreserva = estadoreserva.id_estado_reserva
            ORDER BY r.data_inicio DESC
            LIMIT 5
        """)
        reservas_recentes = cursor.fetchall()

    return render(request, 'admin_dashboard.html', {
        'total_viaturas': total_viaturas,
        'total_reservas': total_reservas,
        'manutencoes_pendentes': manutencoes_pendentes,
        'total_danos': total_danos,
        'total_pecas': total_pecas,
        'total_viaturas_reserva': total_viaturas_reserva,
        'reservas_recentes': reservas_recentes
    })

def admin_viaturas(request):
    marca = request.GET.get('marca', '')
    modelo = request.GET.get('modelo', '')
    tipo = request.GET.get('tipo', '')

    with connection.cursor() as cursor:
        
        query = """
            SELECT
                v.id_viatura,
                marca.nome,
                modelo.nome,
                tipoviatura.nome,
                v.matricula,
                v.preco,
                v.iuc,
                v.inspecao,
                v.km,
                v.ano
            FROM viatura v
            LEFT JOIN marca ON v.id_marca = marca.id_marca
            LEFT JOIN modelo ON v.id_modelo = modelo.id_modelo
            LEFT JOIN tipoviatura ON v.id_tipo_viatura = tipoviatura.id_tipoviatura
        """
        params = []

        cursor.execute(query, params)
        viaturas = cursor.fetchall()

        # Passar os dados para o template
        context = {
            'viaturas': viaturas
        }

    return render(request, 'admin_viaturas.html', context)

def admin_reservas(request):
    estado = request.GET.get('estado', '')
    ordenar = request.GET.get('ordenar', '')

    with connection.cursor() as cursor:
        # Consultar os contadores de estado
        cursor.execute("SELECT COUNT(*) FROM reserva WHERE id_estadoreserva = 1")
        reservas_pendentes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM reserva WHERE id_estadoreserva = 2")
        reservas_confirmadas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM reserva WHERE id_estadoreserva = 3")
        reservas_em_progresso = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM reserva WHERE id_estadoreserva = 4")
        reservas_finalizadas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM reserva WHERE id_estadoreserva = 5")
        reservas_canceladas = cursor.fetchone()[0]

        # Construir a consulta base com JOINs para nome da viatura e utilizador
        query = """
            SELECT 
                r.id_reserva,
                r.data_inicio,
                r.data_fim,
                r.danos,
                r.danostexto,
                r.kmpercorridos,
                CONCAT(marca.nome, ' ', modelo.nome) AS nome_viatura,
                utilizador.nome AS nome_utilizador,
                r.id_estadoreserva
            FROM reserva r
            LEFT JOIN viatura v ON r.id_viatura = v.id_viatura
            LEFT JOIN marca ON v.id_marca = marca.id_marca
            LEFT JOIN modelo ON v.id_modelo = modelo.id_modelo
            LEFT JOIN utilizador ON r.id_utilizador = utilizador.id_utilizador
        """
        params = []

        # Adicionar filtro por estado
        if estado:
            query += " WHERE r.id_estadoreserva = %s"
            params.append(estado)

        # Adicionar ordenação
        if ordenar == "data_inicio_asc":
            query += " ORDER BY r.data_inicio ASC"
        elif ordenar == "data_inicio_desc":
            query += " ORDER BY r.data_inicio DESC"
        elif ordenar == "data_fim_asc":
            query += " ORDER BY r.data_fim ASC"
        elif ordenar == "data_fim_desc":
            query += " ORDER BY r.data_fim DESC"
        else:
            # Ordem padrão por ID da reserva
            query += " ORDER BY r.id_reserva ASC"

        # Executar a consulta
        cursor.execute(query, params)
        reservas = cursor.fetchall()

    # Passar os dados para o template
    context = {
        'reservas_pendentes': reservas_pendentes,
        'reservas_confirmadas': reservas_confirmadas,
        'reservas_em_progresso': reservas_em_progresso,
        'reservas_finalizadas': reservas_finalizadas,
        'reservas_canceladas': reservas_canceladas,
        'reservas': reservas,
        'estado': estado,  # Manter o estado atual no filtro
        'ordenar': ordenar,  # Manter a ordenação atual no filtro
    }

    return render(request, 'admin_reservas.html', context)

def admin_manutencoes(request):
    with connection.cursor() as cursor:
        # Consulta para buscar os dados das manutenções
        query = """
            SELECT 
                m.id_manutencao,
                m.valor,
                m.descricao,
                m.data,
                CONCAT(marca.nome, ' ', modelo.nome) AS nome_viatura
            FROM manutencao m
            LEFT JOIN viatura v ON m.id_viatura = v.id_viatura
            LEFT JOIN marca ON v.id_marca = marca.id_marca
            LEFT JOIN modelo ON v.id_modelo = modelo.id_modelo
        """
        cursor.execute(query)
        manutencoes = cursor.fetchall()

    # Passar os dados para o template
    context = {
        'manutencoes': manutencoes
    }

    return render(request, 'admin_manutencoes.html', context)

def admin_administracao(request):
    return render(request, 'admin_administracao.html')

def admin_marcaslist(request):
    
    marcas = bd.getAllMarcas()
    
    # Retorna a lista de viaturas para o template
    return render(request, 'admin_marcaslist.html', {'marcas': marcas})

def admin_marcadelete(request, marcaid):
    
    bd.deleteMarcaById(marcaid)
        
    return redirect('admin_marcaslist')