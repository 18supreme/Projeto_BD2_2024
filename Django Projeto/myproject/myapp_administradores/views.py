from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, DatabaseError
from django.contrib import messages
from . import basededados as bd
from pymongo import MongoClient
import datetime

# ---| Ligação ao MongoDB |---
client = MongoClient('mongodb://localhost:27017/')
db = client['BD2Projeto']
logs_collection = db['logs']

def salvar_log_mongo(mensagem):
    log_entry = {
        'mensagem': mensagem,
        'data_hora': datetime.datetime.now(),
        'tipo': 'evento'
    }
    
    logs_collection.insert_one(log_entry)

def consultar_logs(request):
    logs = logs_collection.find()
    logs = list(logs)
    
    return render(request, 'logs.html', {'logs': logs})


# ---| Administrador |---
def admin_home(request):
    user_id = request.session.get('ID_user')

    with connection.cursor() as cursor:
        # Contar o total de viaturas
        cursor.execute("SELECT COUNT(*) FROM viatura")
        total_viaturas = cursor.fetchone()[0]

        # Contar o total de reservas
        cursor.execute("SELECT COUNT(*) FROM reserva")
        total_reservas = cursor.fetchone()[0]

        # ---| Manutenções |---
        from datetime import datetime
        # Contar todas as manutenções criadas
        manutencoes_pendentes = logs_collection.count_documents(
            {'mensagem': {'$regex': '.*Manutenção.*criada.*', '$options': 'i'}}
        )
        # Contar todas as manutenções eliminadas
        manutencoes_eliminadas = logs_collection.count_documents(
            {'mensagem': {'$regex': '.*Manutenção.*eliminada.*', '$options': 'i'}}
        )
        # Subtrair manutenções eliminadas do total
        manutencoes_pendentes -= manutencoes_eliminadas

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

def admin_administracao(request):
    return render(request, 'admin_administracao.html')


# ---| Viaturas |---
def admin_viaturas(request):
    marca_filtro = request.GET.get('marca', '')
    modelo_filtro = request.GET.get('modelo', '')
    tipo_filtro = request.GET.get('tipo', '')

    where_clauses = []
    params = []

    if marca_filtro:
        where_clauses.append("marca.id_marca = %s")
        params.append(marca_filtro)

    if modelo_filtro:
        where_clauses.append("modelo.id_modelo = %s")
        params.append(modelo_filtro)

    if tipo_filtro:
        where_clauses.append("tipoviatura.id_tipoviatura = %s")
        params.append(tipo_filtro)

    where_clause = " AND ".join(where_clauses)
    where_clause = f"WHERE {where_clause}" if where_clause else ""

    query = f"""
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
        {where_clause}
    """

    with connection.cursor() as cursor:
        # Obter marcas
        cursor.execute("SELECT id_marca, nome FROM marca")
        marcas = cursor.fetchall()

        # Obter modelos
        cursor.execute("SELECT id_modelo, nome FROM modelo")
        modelos = cursor.fetchall()

        # Obter tipos de viatura
        cursor.execute("SELECT id_tipoviatura, nome FROM tipoviatura")
        tipos = cursor.fetchall()

        # Executar a query de viaturas com os filtros aplicados
        cursor.execute(query, params)
        viaturas = cursor.fetchall()

    context = {
        'viaturas': viaturas,
        'marcas': marcas,
        'modelos': modelos,
        'tipos': tipos,
        'filtros': {
            'marca': marca_filtro,
            'modelo': modelo_filtro,
            'tipo': tipo_filtro,
        }
    }
    return render(request, 'admin_viaturas.html', context)

def admin_viaturas_create(request):
    if request.method == 'POST':
        matricula = request.POST['matricula']
        ano = request.POST['ano']
        km = request.POST['km']
        cilindrada = request.POST['cilindrada']
        potencia = request.POST['potencia']
        portas = request.POST['portas']
        lotacao = request.POST['lotacao']
        numero_mudancas = request.POST['numero_mudancas']
        inspecao = request.POST['inspecao']
        iuc = request.POST['iuc']
        preco = request.POST['preco']
        marca_id = request.POST['marca']
        modelo_id = request.POST['modelo']
        tipo_viatura_id = request.POST['tipo_viatura']
        estado_viatura_id = request.POST['estado_viatura']
        combustivel_id = request.POST['combustivel']
        caixa_id = request.POST['caixa']
        traccao_id = request.POST['traccao']
        cor_id = request.POST.get('cor')  # Adicionar a cor

        # Chamar o procedimento armazenado com os parâmetros
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    CALL registar_Viatura(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )""", [
                        matricula, ano, km, cilindrada, potencia, portas, lotacao,
                        numero_mudancas, inspecao, iuc, preco, traccao_id, caixa_id,
                        combustivel_id, tipo_viatura_id, marca_id, modelo_id, cor_id, estado_viatura_id
                    ])

                # Se tudo correr bem, redirecionamos para a página de viaturas
                return redirect('admin_viaturas')
            except Exception as e:
                # Se houver um erro, pode ser capturado aqui
                return render(request, 'admin_viaturas_create.html', {'error': str(e)})

    else:
        # Obter dados para preencher os campos do formulário
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Marca, Nome FROM Marca WHERE IsActive = TRUE;")
            marcas = cursor.fetchall()

            cursor.execute("SELECT ID_Modelo, Nome FROM Modelo WHERE IsActive = TRUE;")
            modelos = cursor.fetchall()

            cursor.execute("SELECT ID_TipoViatura, Nome FROM TipoViatura WHERE IsActive = TRUE;")
            tipos_viatura = cursor.fetchall()

            cursor.execute("SELECT ID_EstadoViatura, Estado FROM EstadoViatura WHERE IsActive = TRUE;")
            estados_viatura = cursor.fetchall()

            cursor.execute("SELECT ID_Combustivel, Nome FROM Combustivel WHERE IsActive = TRUE;")
            combustiveis = cursor.fetchall()

            cursor.execute("SELECT ID_Caixa, Nome FROM TipoCaixa WHERE IsActive = TRUE;")
            caixas = cursor.fetchall()

            cursor.execute("SELECT ID_Traccao, Nome FROM Traccao WHERE IsActive = TRUE;")
            traccoes = cursor.fetchall()

            cursor.execute("SELECT ID_Cor, Nome FROM Cores WHERE IsActive = TRUE;")
            cores = cursor.fetchall()  # Obter as cores

        return render(request, 'admin_viaturas_create.html', {
            'marcas': marcas,
            'modelos': modelos,
            'tipos_viatura': tipos_viatura,
            'estados_viatura': estados_viatura,
            'combustiveis': combustiveis,
            'caixas': caixas,
            'traccoes': traccoes,
            'cores': cores,  # Passar as cores para o template
        })

def admin_viaturas_edit(request, viatura_id):
    if not viatura_id:
        return redirect('admin_viaturas')

    with connection.cursor() as cursor:
        try:
            if request.method == 'GET':
                # Recuperar dados da viatura com o ID fornecido
                cursor.execute("""
                    SELECT
                        v.id_viatura, v.matricula, v.ano, v.km, v.cilindrada, v.potencia, v.portas,
                        v.lotacao, v.numeromudancas, v.inspecao, v.iuc, v.preco, v.id_marca, 
                        v.id_modelo, v.id_tipo_viatura, v.id_estado_viatura, v.id_combustivel, 
                        v.id_tipocaixa, v.id_traccao, v.id_cor
                    FROM viatura v
                    WHERE v.id_viatura = %s
                """, [viatura_id])
                
                viatura = cursor.fetchone()

                if not viatura:
                    return redirect('admin_viaturas')

                # Mostrar valores para verificar se estão corretos
                print("Valores recuperados da base de dados:")
                print(f"iuc: {viatura[10]}, preco: {viatura[11]}")

                # Recuperar a data da inspeção, se existir
                inspecao = viatura[9].strftime('%Y-%m-%d') if viatura[9] else None

                # Limpar qualquer caractere não numérico como o símbolo $
                def limpar_valor(valor):
                    if valor:
                        return ''.join(c for c in str(valor) if c.isdigit() or c == '.')
                    return '0.00'

                # Limpeza dos valores de IUC e Preço
                iuc = limpar_valor(viatura[10])
                preco = limpar_valor(viatura[11])

                # Mostrar valores após limpeza
                print(f"Após limpeza - iuc: {iuc}, preco: {preco}")

                # Garantir que IUC e Preço são números com 2 casas decimais
                try:
                    iuc = f"{float(iuc):.2f}"
                except (ValueError, TypeError):
                    iuc = "0.00"  # Valor padrão em caso de erro

                try:
                    preco = f"{float(preco):.2f}"
                except (ValueError, TypeError):
                    preco = "0.00"  # Valor padrão em caso de erro

                # Mostrar valores após formatação
                print(f"Após formatação - iuc: {iuc}, preco: {preco}")

                # Obter dados para preencher os campos do formulário
                cursor.execute("SELECT id_marca, nome FROM marca WHERE IsActive = TRUE;")
                marcas = cursor.fetchall()

                cursor.execute("SELECT id_modelo, nome FROM modelo WHERE IsActive = TRUE;")
                modelos = cursor.fetchall()

                cursor.execute("SELECT id_tipoviatura, nome FROM tipoviatura WHERE IsActive = TRUE;")
                tipos_viatura = cursor.fetchall()

                cursor.execute("SELECT id_estadoviatura, estado FROM estadoviatura WHERE IsActive = TRUE;")
                estados_viatura = cursor.fetchall()

                cursor.execute("SELECT id_combustivel, nome FROM combustivel WHERE IsActive = TRUE;")
                combustiveis = cursor.fetchall()

                cursor.execute("SELECT id_caixa, nome FROM tipocaixa WHERE IsActive = TRUE;")
                caixas = cursor.fetchall()

                cursor.execute("SELECT id_traccao, nome FROM traccao WHERE IsActive = TRUE;")
                traccoes = cursor.fetchall()

                cursor.execute("SELECT id_cor, nome FROM cores WHERE IsActive = TRUE;")
                cores = cursor.fetchall()

                # Passar os dados para o template
                return render(request, 'admin_viaturas_edit.html', {
                    'viatura': viatura,
                    'inspecao': inspecao,
                    'iuc': iuc,
                    'preco': preco,
                    'marcas': marcas,
                    'modelos': modelos,
                    'tipos_viatura': tipos_viatura,
                    'estados_viatura': estados_viatura,
                    'combustiveis': combustiveis,
                    'caixas': caixas,
                    'traccoes': traccoes,
                    'cores': cores,
                })

            elif request.method == 'POST':
                matricula = request.POST['matricula']
                ano = request.POST['ano']
                km = request.POST['km']
                cilindrada = request.POST['cilindrada']
                potencia = request.POST['potencia']
                portas = request.POST['portas']
                lotacao = request.POST['lotacao']
                numero_mudancas = request.POST['numero_mudancas']
                inspecao = request.POST['inspecao']
                iuc = request.POST['iuc']
                preco = request.POST['preco']
                marca_id = request.POST['marca']
                modelo_id = request.POST['modelo']
                tipo_viatura_id = request.POST['tipo_viatura']
                estado_viatura_id = request.POST['estado_viatura']
                combustivel_id = request.POST['combustivel']
                caixa_id = request.POST['caixa']
                traccao_id = request.POST['traccao']
                cor_id = request.POST.get('cor')  # A cor da viatura (opcional)

                # Atualizar os dados da viatura
                cursor.execute("""
                    UPDATE viatura
                    SET matricula = %s, ano = %s, km = %s, cilindrada = %s, potencia = %s,
                        portas = %s, lotacao = %s, numeromudancas = %s, inspecao = %s, 
                        iuc = %s, preco = %s, id_marca = %s, id_modelo = %s, 
                        id_tipo_viatura = %s, id_estado_viatura = %s, id_combustivel = %s, 
                        id_traccao = %s, id_tipocaixa = %s, id_cor = %s
                    WHERE id_viatura = %s
                """, [
                    matricula, ano, km, cilindrada, potencia, portas, lotacao, numero_mudancas,
                    inspecao, iuc, preco, marca_id, modelo_id, tipo_viatura_id, estado_viatura_id,
                    combustivel_id, traccao_id, caixa_id, cor_id, viatura_id
                ])

                return redirect('admin_viaturas')

        except Exception as e:
            print(f"Erro ao editar ou atualizar viatura: {e}")
            return redirect('admin_viaturas')

def admin_viaturas_delete(request, viatura_id):
    try:
        # Verifica se o viatura_id foi passado corretamente
        if not viatura_id:
            return redirect('admin_viaturas')  # Se o ID não for válido, redireciona para a página de viaturas
        
        # Eliminar a viatura com o id fornecido
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM viatura WHERE id_viatura = %s", [viatura_id])

        # Redireciona para a lista de viaturas após a eliminação
        return redirect('admin_viaturas')
    except Exception as e:
        # Em caso de erro, exibe o erro e redireciona para a página de viaturas
        print(f"Erro ao eliminar viatura: {e}")
        return redirect('admin_viaturas')


# ---| Reservas |---
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

def admin_reservas_create(request):
    if request.method == 'POST':
        data_inicio = request.POST['data_inicio']
        data_fim = request.POST['data_fim']
        danos = 'damaged' in request.POST  # Se a opção "Danos" estiver marcada
        danos_texto = request.POST['danos_texto']
        km_percorridos = request.POST['km_percorridos']
        id_viatura = request.POST['viatura']
        id_utilizador = request.POST['utilizador']
        id_estado_reserva = request.POST['estado_reserva']

        # Chamar o procedimento armazenado para registrar a reserva
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    CALL registar_Reserva(
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )""", [
                        data_inicio, data_fim, danos, danos_texto, km_percorridos,
                        id_viatura, id_utilizador, id_estado_reserva
                    ])

                return redirect('admin_reservas')
            except Exception as e:
                return render(request, 'admin_reservas_create.html', {'error': str(e)})

    else:
        # Buscar as viaturas com Marca + Modelo para o dropdown
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT v.id_viatura, CONCAT(marca.nome, ' ', modelo.nome) AS nome_viatura
                FROM viatura v
                JOIN marca ON v.id_marca = marca.id_marca
                JOIN modelo ON v.id_modelo = modelo.id_modelo
            """)
            viaturas = cursor.fetchall()

            # Buscar utilizadores e estados de reserva como no exemplo da manutenção
            cursor.execute("""
                SELECT ID_Estado_Reserva, Estado 
                FROM EstadoReserva 
                WHERE IsActive = TRUE;
            """)
            estados_reserva = cursor.fetchall()

            cursor.execute("SELECT ID_Utilizador, Nome FROM Utilizador WHERE IsActive = TRUE;")
            utilizadores = cursor.fetchall()

        return render(request, 'admin_reservas_create.html', {
            'viaturas': viaturas,
            'utilizadores': utilizadores,
            'estados_reserva': estados_reserva,
        })

def admin_reservas_edit(request, reserva_id):
    if not reserva_id:
        return redirect('admin_reservas')

    with connection.cursor() as cursor:
        try:
            if request.method == 'GET':
                # Recuperar dados da reserva com o ID fornecido e incluir dados do utilizador
                cursor.execute("""
                    SELECT r.id_reserva, r.data_inicio, r.data_fim, r.danos, r.danostexto, r.kmpercorridos, 
                           r.id_viatura, r.id_utilizador, r.id_estadoreserva, u.nome AS nome_utilizador
                    FROM reserva r
                    JOIN utilizador u ON r.id_utilizador = u.id_utilizador
                    WHERE r.id_reserva = %s
                """, [reserva_id])

                reserva = cursor.fetchone()

                if not reserva:
                    return redirect('admin_reservas')

                # Obter todos os dados necessários para preencher os campos do formulário
                cursor.execute("SELECT id_viatura, matricula FROM viatura;")
                viaturas = cursor.fetchall()

                cursor.execute("SELECT id_estado_reserva, estado FROM estadoreserva WHERE IsActive = TRUE;")
                estados_reserva = cursor.fetchall()

                # Passar os dados para o template
                return render(request, 'admin_reservas_edit.html', {
                    'reserva': reserva,
                    'viaturas': viaturas,
                    'estados_reserva': estados_reserva,
                })

            elif request.method == 'POST':
                data_inicio = request.POST['data_inicio']
                data_fim = request.POST['data_fim']
                danos = request.POST['danos']
                danostexto = request.POST['danostexto']
                kmpercorridos = request.POST['kmpercorridos']
                id_viatura = request.POST['viatura']
                id_utilizador = request.POST['utilizador']
                id_estadoreserva = request.POST['estadoreserva']

                # Atualizar os dados da reserva
                cursor.execute("""
                    UPDATE reserva
                    SET data_inicio = %s, data_fim = %s, danos = %s, danostexto = %s, kmpercorridos = %s,
                        id_viatura = %s, id_utilizador = %s, id_estadoreserva = %s
                    WHERE id_reserva = %s
                """, [
                    data_inicio, data_fim, danos, danostexto, kmpercorridos, id_viatura,
                    id_utilizador, id_estadoreserva, reserva_id
                ])

                # Redirecionar para a página de reservas após a atualização
                return redirect('admin_reservas')

        except Exception as e:
            print(f"Erro ao editar ou atualizar reserva: {e}")
            return redirect('admin_reservas')

def admin_reservas_delete(request, reserva_id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM Reserva 
                    WHERE ID_Reserva = %s;
                """, [reserva_id])
            return redirect('admin_reservas')
        except Exception as e:
            return redirect('admin_reservas')
    return redirect('admin_reservas')


# ---| Manutenções |---
def admin_manutencoes(request):
    with connection.cursor() as cursor:
        # Consulta para buscar os dados das manutenções
        query = """
            SELECT 
                m.id_manutencao,
                m.valor,
                m.descricao,
                m.data,
                marca.nome AS marca,
                modelo.nome AS modelo
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

def listar_manutencoes(request):
    viatura_id = request.GET.get("viatura", "")
    data = request.GET.get("data", "")
    valor = request.GET.get("valor", "")

    query = """
        SELECT m.id_manutencao, m.valor, m.descricao, m.data, ma.nome AS marca, mo.nome AS modelo
        FROM manutencao m
        JOIN viatura v ON m.id_viatura = v.id_viatura
        JOIN modelo mo ON v.id_modelo = mo.id_modelo
        JOIN marca ma ON v.id_marca = ma.id_marca
        WHERE 1=1
    """
    params = []

    if viatura_id:
        query += " AND m.id_viatura = %s"
        params.append(viatura_id)

    if data:
        query += " AND m.data = %s"
        params.append(data)

    if valor:
        query += " AND m.valor <= %s"
        params.append(valor)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        manutencoes = cursor.fetchall()

    # Buscar todas as viaturas para popular o filtro corretamente
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT v.id_viatura, ma.nome AS marca, mo.nome AS modelo
            FROM viatura v
            JOIN modelo mo ON v.id_modelo = mo.id_modelo
            JOIN marca ma ON v.id_marca = ma.id_marca;
        """)
        viaturas = cursor.fetchall()

    filtros = {
        "viatura": viatura_id,
        "data": data,
        "valor": valor
    }

    return render(request, "admin_manutencoes.html", {
        "manutencoes": manutencoes,
        "viaturas": viaturas,
        "filtros": filtros
    })

def criar_manutencao(request):
    if request.method == "POST":
        viatura_id = request.POST.get("viatura")
        valor = request.POST.get("valor")
        descricao = request.POST.get("descricao")
        data = request.POST.get("data")

        with connection.cursor() as cursor:
            cursor.execute(
                "CALL registar_Manutencao(%s, %s, %s, %s)",
                [valor, descricao, data, viatura_id]
            )

        salvar_log_mongo(f"Manutenção criada para a viatura ID {viatura_id} com valor {valor}.")

        return redirect("admin_manutencoes")

    # Buscar as viaturas com Marca + Modelo para o dropdown
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT v.id_viatura, CONCAT(marca.nome, ' ', modelo.nome) AS nome_viatura
            FROM viatura v
            JOIN marca ON v.id_marca = marca.id_marca
            JOIN modelo ON v.id_modelo = modelo.id_modelo
        """)
        viaturas = cursor.fetchall()

    return render(request, "admin_manutencoes_create.html", {"viaturas": viaturas})

def editar_manutencao(request, manutencao_id):
    # Verifica se o método da requisição é POST (submissão do formulário)
    if request.method == "POST":
        viatura_id = request.POST.get("viatura")
        valor = request.POST.get("valor")
        descricao = request.POST.get("descricao")
        data = request.POST.get("data")

        # Atualiza os dados da manutenção no banco de dados
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE manutencao
                SET id_viatura = %s, valor = %s, descricao = %s, data = %s
                WHERE id_manutencao = %s
                """,
                [viatura_id, valor, descricao, data, manutencao_id],
            )

        salvar_log_mongo(f"Manutenção com ID {manutencao_id} editada para a viatura ID {viatura_id}.")
        
        return redirect("admin_manutencoes")  # Redireciona para a lista de manutenções

    # Buscar os dados da manutenção a ser editada
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id_manutencao, id_viatura, valor, descricao, data
            FROM manutencao
            WHERE id_manutencao = %s
            """,
            [manutencao_id],
        )
        manutencao = cursor.fetchone()

    # Se a manutenção não for encontrada, redireciona para a lista
    if not manutencao:
        return redirect("admin_manutencoes")

    # Formatar a data para o formato 'YYYY-MM-DD' necessário para o campo <input type="date">
    manutencao_data = manutencao[4]
    if manutencao_data:
        manutencao_data = manutencao_data.strftime('%Y-%m-%d')  # Formato 'YYYY-MM-DD'

    # Buscar as viaturas para o dropdown (agora com Marca + Modelo)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT v.id_viatura, CONCAT(m.nome, ' ', mo.nome) AS marca_modelo
            FROM viatura v
            JOIN marca m ON v.id_marca = m.id_marca
            JOIN modelo mo ON v.id_modelo = mo.id_modelo
            """
        )
        viaturas = cursor.fetchall()

    # Passa os dados para o template
    return render(
        request,
        "admin_manutencoes_edit.html",  # Template de edição
        {"manutencao": manutencao, "viaturas": viaturas, "manutencao_data": manutencao_data},
    )

def eliminar_manutencao(request, id_manutencao):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Manutencao WHERE ID_Manutencao = %s", [id_manutencao])

    salvar_log_mongo(f"Manutenção com ID {id_manutencao} eliminada.")
    
    return redirect('admin_manutencoes')


# ---| Marcas |---
def admin_marcaslist(request):
    with connection.cursor() as cursor:
        # Consulta SQL para obter as marcas
        cursor.execute("SELECT ID_Marca, Nome, IsActive FROM Marca")
        marcas = cursor.fetchall()

    context = {'marcas': marcas}
    return render(request, 'admin_marcaslist.html', context)

def admin_marcacreate(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        is_active = request.POST.get("is_active")

        is_active = True if is_active == "on" else False  # Converte para Booleano

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL registar_Marca(%s, %s)", [nome, is_active])  # Chama o PROCEDURE
            return redirect('admin_marcaslist')

        except DatabaseError as e:
            error_message = "Erro: A marca já existe!" if "já existe" in str(e) else "Erro ao criar a marca!"
            return render(request, 'admin_marcas_create.html', {"error": error_message})

    return render(request, 'admin_marcas_create.html')

def admin_marcaedit(request, marcaid):
    if request.method == "POST":
        nome = request.POST.get("nome")
        is_active = request.POST.get("is_active")

        # Converter checkbox para Booleano
        is_active = True if is_active == "on" else False  

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL update_Marca(%s, %s, %s)", [marcaid, nome, is_active])
            return redirect('admin_marcaslist')

        except DatabaseError as e:
            error_message = "Erro: Já existe uma outra marca com este nome!" if "já existe" in str(e) else "Erro ao editar a marca!"
            return render(request, 'admin_marcas_edit.html', {"marcaid": marcaid, "marca": (nome, is_active), "error": error_message})

    # Obter os dados da marca para exibir no formulário
    with connection.cursor() as cursor:
        cursor.execute("SELECT Nome, IsActive FROM Marca WHERE ID_Marca = %s", [marcaid])
        marca = cursor.fetchone()

    return render(request, 'admin_marcas_edit.html', {"marcaid": marcaid, "marca": marca})

def admin_marcadelete(request, marcaid):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                # Chama o procedimento armazenado no PostgreSQL
                cursor.execute("CALL deleteMarcaById(%s)", [marcaid])
            return redirect('admin_marcaslist')  # Redireciona para a lista após a eliminação
        except Exception as e:
            print(f"Erro ao eliminar a marca: {e}")
            return redirect('admin_marcaslist')

    # Se o método não for POST, redireciona para evitar erro
    return redirect('admin_marcaslist')


# ---| Modelos |---
def admin_modeloslist(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.ID_Modelo, m.Nome, ma.Nome, m.IsActive 
            FROM Modelo m 
            INNER JOIN Marca ma ON m.ID_Marca = ma.ID_Marca
            ORDER BY ma.Nome, m.Nome
        """)
        modelos = cursor.fetchall()

    return render(request, 'admin_modelos_list.html', {'modelos': modelos})

def admin_modelocreate(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        id_marca = request.POST.get("id_marca")
        is_active = request.POST.get("is_active")

        is_active = True if is_active == "on" else False  

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL registar_Modelo(%s, %s, %s)", [nome, id_marca, is_active])
            return redirect('admin_modeloslist')
        except DatabaseError as e:
            error_message = "Erro: O modelo já existe para esta marca!" if "já existe" in str(e) else "Erro ao criar o modelo!"
            return render(request, 'admin_modelos_create.html', {"error": error_message})

    # Buscar marcas para dropdown
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Marca, Nome FROM Marca")
        marcas = cursor.fetchall()

    return render(request, 'admin_modelos_create.html', {'marcas': marcas})

def admin_modeloedit(request, modelo_id):
    if request.method == "POST":
        nome = request.POST.get("nome")
        id_marca = request.POST.get("id_marca")
        is_active = request.POST.get("is_active")

        is_active = True if is_active == "on" else False  

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL update_Modelo(%s, %s, %s, %s)", [modelo_id, nome, id_marca, is_active])
            return redirect('admin_modeloslist')
        except DatabaseError as e:
            error_message = "Erro: Já existe outro modelo com este nome para esta marca!" if "já existe" in str(e) else "Erro ao editar o modelo!"
            return render(request, 'admin_modelos_edit.html', {"modelo_id": modelo_id, "modelo": (nome, id_marca, is_active), "error": error_message})

    with connection.cursor() as cursor:
        cursor.execute("SELECT Nome, ID_Marca, IsActive FROM Modelo WHERE ID_Modelo = %s", [modelo_id])
        modelo = cursor.fetchone()

        cursor.execute("SELECT ID_Marca, Nome FROM Marca")
        marcas = cursor.fetchall()

    return render(request, 'admin_modelos_edit.html', {"modelo_id": modelo_id, "modelo": modelo, "marcas": marcas})

def admin_modelodelete(request, modelo_id):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL delete_Modelo(%s)", [modelo_id])
            return redirect('admin_modeloslist')
        except Exception as e:
            print(f"Erro ao eliminar modelo: {e}")
            return redirect('admin_modeloslist')

    return redirect('admin_modeloslist')

# Selecionar cor 
def admin_coreslist(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Cor, Nome, IsActive FROM Cores ORDER BY Nome")
        cores = cursor.fetchall()

    return render(request, 'admin_cores_list.html', {'cores': cores})

# Criar Cor
def admin_corcreate(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        is_active = request.POST.get("is_active")

        is_active = True if is_active == "on" else False  

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL registar_Cor(%s, %s)", [nome, is_active])
            return redirect('admin_coreslist')
        except DatabaseError as e:
            error_message = "Erro: A cor já existe!" if "já existe" in str(e) else "Erro ao criar a cor!"
            return render(request, 'admin_cores_create.html', {"error": error_message})

    return render(request, 'admin_cores_create.html')

#Editar Cor  
def admin_coredit(request, cor_id):
    if request.method == "POST":
        nome = request.POST.get("nome")
        is_active = request.POST.get("is_active")

        is_active = True if is_active == "on" else False  

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL update_Cor(%s, %s, %s)", [cor_id, nome, is_active])
            return redirect('admin_coreslist')
        except DatabaseError as e:
            error_message = "Erro: Já existe outra cor com este nome!" if "já existe" in str(e) else "Erro ao editar a cor!"
            return render(request, 'admin_cores_edit.html', {"cor_id": cor_id, "cor": (nome, is_active), "error": error_message})

    with connection.cursor() as cursor:
        cursor.execute("SELECT Nome, IsActive FROM Cores WHERE ID_Cor = %s", [cor_id])
        cor = cursor.fetchone()

    return render(request, 'admin_cores_edit.html', {"cor_id": cor_id, "cor": cor})

#Apagar Cor 
def admin_cordelete(request, cor_id):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL delete_Cor(%s)", [cor_id])
            return redirect('admin_coreslist')
        except Exception as e:
            print(f"Erro ao eliminar cor: {e}")
            return redirect('admin_coreslist')

    return redirect('admin_coreslist')


#Listar combustiveis

def admin_combustiveislist(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Combustivel, Nome, IsActive FROM Combustivel ORDER BY Nome")
        combustiveis = cursor.fetchall()

    return render(request, 'admin_combustiveis_list.html', {'combustiveis': combustiveis})

#Criar combustiveis 
def admin_combustivelcreate(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        is_active = request.POST.get("is_active")

        is_active = True if is_active == "on" else False  

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL registar_Combustivel(%s, %s)", [nome, is_active])
            return redirect('admin_combustiveislist')

        except DatabaseError as e:
            error_message = "Erro: O combustível já existe!" if "O combustível" in str(e) else "Erro ao criar o combustível!"
            return render(request, 'admin_combustiveis_create.html', {"error": error_message})

    return render(request, 'admin_combustiveis_create.html')

#Editar combustiveis 
def admin_combustiveledit(request, combustivel_id):
    if request.method == "POST":
        nome = request.POST.get("nome")
        is_active = request.POST.get("is_active")

        # Converter o checkbox corretamente para True ou False
        is_active = True if is_active == "on" else False  

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL update_Combustivel(%s, %s, %s)", [combustivel_id, nome, is_active])
            return redirect('admin_combustiveislist')
        except DatabaseError as e:
            error_message = "Erro: Já existe outro combustível com este nome!" if "já existe" in str(e) else "Erro ao editar o combustível!"
            return render(request, 'admin_combustiveis_edit.html', {"combustivel_id": combustivel_id, "combustivel": (nome, is_active), "error": error_message})

    with connection.cursor() as cursor:
        cursor.execute("SELECT Nome, IsActive FROM Combustivel WHERE ID_Combustivel = %s", [combustivel_id])
        combustivel = cursor.fetchone()

    return render(request, 'admin_combustiveis_edit.html', {"combustivel_id": combustivel_id, "combustivel": combustivel})


#Eliminar Combustiveis 
def admin_combustiveldelete(request, combustivel_id):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL delete_Combustivel(%s)", [combustivel_id])
            return redirect('admin_combustiveislist')
        except Exception as e:
            print(f"Erro ao eliminar combustível: {e}")
            return redirect('admin_combustiveislist')

    return redirect('admin_combustiveislist')


#Listar Fornecedores 
def admin_fornecedoreslist(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Fornecedor, Nome, Valor, IsActive FROM Fornecedor ORDER BY Nome")
        fornecedores = cursor.fetchall()

    return render(request, 'admin_fornecedores_list.html', {'fornecedores': fornecedores})


#Criar Fornecedor 
def admin_fornecedorcreate(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        valor = request.POST.get("valor")
        is_active = request.POST.get("is_active")

        is_active = True if is_active == "on" else False  

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL registar_Fornecedor(%s, %s, %s)", [nome, valor, is_active])
            return redirect('admin_fornecedoreslist')

        except DatabaseError as e:
            error_message = "Erro: O fornecedor já existe!" if "O fornecedor" in str(e) else "Erro ao criar o fornecedor!"
            return render(request, 'admin_fornecedores_create.html', {"error": error_message})

    return render(request, 'admin_fornecedores_create.html')


#Editar Fornecedor 
def admin_fornecedoredit(request, fornecedor_id):
    if request.method == "POST":
        nome = request.POST.get("nome")
        valor = request.POST.get("valor")
        is_active = request.POST.get("is_active")

        is_active = True if is_active == "on" else False  

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL update_Fornecedor(%s, %s, %s, %s)", [fornecedor_id, nome, valor, is_active])
            return redirect('admin_fornecedoreslist')
        except DatabaseError as e:
            error_message = "Erro: Já existe outro fornecedor com este nome!" if "já existe" in str(e) else "Erro ao editar o fornecedor!"
            return render(request, 'admin_fornecedores_edit.html', {"fornecedor_id": fornecedor_id, "fornecedor": (nome, valor, is_active), "error": error_message})

    with connection.cursor() as cursor:
        cursor.execute("SELECT Nome, Valor, IsActive FROM Fornecedor WHERE ID_Fornecedor = %s", [fornecedor_id])
        fornecedor = cursor.fetchone()

    return render(request, 'admin_fornecedores_edit.html', {"fornecedor_id": fornecedor_id, "fornecedor": fornecedor})


#Eliminar Fornecedor 
def admin_fornecedordelete(request, fornecedor_id):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL delete_Fornecedor(%s)", [fornecedor_id])
            return redirect('admin_fornecedoreslist')
        except DatabaseError as e:  # Captura erros do PostgreSQL
            error_message = str(e)
            print(f"Erro ao eliminar fornecedor: {error_message}")  # Debug no terminal Django

            if "O fornecedor tem encomendas associadas" in error_message:
                messages.error(request, "O fornecedor tem encomendas associadas e não pode ser eliminado.")
            else:
                messages.error(request, "Erro ao eliminar fornecedor. Tente novamente.")

        return redirect('admin_fornecedoreslist')

    return redirect('admin_fornecedoreslist')


# Listar encomendas
def admin_encomendaslist(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e.ID_Encomenda_Fornecedor, f.Nome, p.Nome, e.Quantidade, e.Valor, ef.Estado
            FROM EncomendaFornecedor e
            JOIN Fornecedor f ON e.ID_Fornecedor = f.ID_Fornecedor
            JOIN Pecas p ON e.ID_Peca = p.ID_Peca
            JOIN EstadoEncomendaFornecedor ef ON e.ID_EstadoEncomenda = ef.ID_EstadoEncomenda
            ORDER BY e.ID_Encomenda_Fornecedor
        """)
        encomendas = cursor.fetchall()

    return render(request, 'admin_encomendas_list.html', {'encomendas': encomendas})


# Criar EncomendaFornecedor
def admin_encomendacreate(request):
    if request.method == "POST":
        fornecedor_id = request.POST['fornecedor']
        peca_id = request.POST['peca']
        quantidade = request.POST['quantidade']
        valor = request.POST['valor']
        estado_id = request.POST['estado']
        
        with connection.cursor() as cursor:
            cursor.execute("CALL registar_Encomenda(%s, %s, %s, %s, %s)", 
                           [fornecedor_id, peca_id, quantidade, valor, estado_id])

        return redirect('admin_encomendaslist')

    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Fornecedor, Nome FROM Fornecedor")
        fornecedores = cursor.fetchall()
        
        cursor.execute("SELECT ID_Peca, Nome FROM Pecas")
        pecas = cursor.fetchall()

        cursor.execute("SELECT ID_EstadoEncomenda, Estado FROM EstadoEncomendaFornecedor")
        estados = cursor.fetchall()

    return render(request, 'admin_encomendas_create.html', {
        'fornecedores': fornecedores, 
        'pecas': pecas, 
        'estados': estados
    })

# Editar EncomendaFornecedor
def admin_encomendaedit(request, encomenda_id):
    with connection.cursor() as cursor:
        # Buscar os dados da encomenda
        cursor.execute("""
            SELECT Quantidade, Valor, ID_EstadoEncomenda 
            FROM EncomendaFornecedor
            WHERE ID_Encomenda_Fornecedor = %s
        """, [encomenda_id])
        encomenda = cursor.fetchone()

        # Buscar a lista de estados
        cursor.execute("SELECT ID_EstadoEncomenda, Estado FROM EstadoEncomendaFornecedor")
        estados = cursor.fetchall()

    if request.method == "POST":
        quantidade = request.POST["quantidade"]
        valor = request.POST["valor"]
        estado = request.POST["estado"]

        with connection.cursor() as cursor:
            cursor.execute("CALL update_Encomenda(%s, %s, %s, %s)", 
                           [encomenda_id, quantidade, valor, estado])

        return redirect('admin_encomendaslist')

    return render(request, 'admin_encomendas_edit.html', {
        'encomenda': encomenda,
        'estados': estados
    })



# Eliminar EncomendaFornecedor
def admin_encomendadelete(request, encomenda_id):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL delete_Encomenda(%s)", [encomenda_id])
            return redirect('admin_encomendaslist')
        except Exception as e:
            print(f"Erro ao eliminar encomenda: {e}")

    return redirect('admin_encomendaslist')

# 🔹 Listar Peças
def admin_pecaslist(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.ID_Peca, p.Nome, p.Stock, m.Nome AS Marca, mo.Nome AS Modelo
            FROM Pecas p
            LEFT JOIN Marca m ON p.ID_Marca = m.ID_Marca
            LEFT JOIN Modelo mo ON p.ID_Modelo = mo.ID_Modelo
        """)
        pecas = cursor.fetchall()

    return render(request, "admin_pecas_list.html", {"pecas": pecas})

# 🔹 Criar Peça
def admin_pecacreate(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        stock = request.POST.get("stock", 0)
        id_marca = request.POST.get("id_marca")
        id_modelo = request.POST.get("id_modelo")

        if not id_marca or not id_modelo:
            return render(request, 'admin_pecas_create.html', {
                "error": "Selecione uma marca e um modelo!",
                "marcas": marcas,
                "modelos": modelos
            })

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL registar_Peca(%s, %s, %s, %s)", [nome, stock, id_marca, id_modelo])
            return redirect('admin_pecaslist')

        except Exception as e:
            error_message = "Erro ao criar peça: " + str(e)
            return render(request, 'admin_pecas_create.html', {
                "error": error_message,
                "marcas": marcas,
                "modelos": modelos
            })

    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Marca, Nome FROM Marca ORDER BY Nome")
        marcas = cursor.fetchall()

        cursor.execute("SELECT ID_Modelo, Nome FROM Modelo ORDER BY Nome")
        modelos = cursor.fetchall()

    return render(request, 'admin_pecas_create.html', {"marcas": marcas, "modelos": modelos})

# 🔹 Editar Peça
def admin_pecaedit(request, peca_id):
    if request.method == "POST":
        nome = request.POST.get("nome")
        stock = request.POST.get("stock", 0)
        id_marca = request.POST.get("id_marca")
        id_modelo = request.POST.get("id_modelo")

        if not id_marca or not id_modelo:
            return render(request, 'admin_pecas_edit.html', {
                "error": "Selecione uma marca e um modelo!",
                "peca": (peca_id, nome, stock, id_marca, id_modelo),
                "marcas": marcas,
                "modelos": modelos
            })

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL update_Peca(%s, %s, %s, %s, %s)", [peca_id, nome, stock, id_marca, id_modelo])
            return redirect('admin_pecaslist')

        except Exception as e:
            error_message = "Erro ao atualizar peça: " + str(e)
            return render(request, 'admin_pecas_edit.html', {
                "error": error_message,
                "peca": (peca_id, nome, stock, id_marca, id_modelo),
                "marcas": marcas,
                "modelos": modelos
            })

    with connection.cursor() as cursor:
        # Buscar os dados da peça
        cursor.execute("SELECT Nome, Stock, ID_Marca, ID_Modelo FROM Pecas WHERE ID_Peca = %s", [peca_id])
        peca = cursor.fetchone()

        # Se a peça não for encontrada, redirecionar para a lista
        if not peca:
            return redirect('admin_pecaslist')

        cursor.execute("SELECT ID_Marca, Nome FROM Marca ORDER BY Nome")
        marcas = cursor.fetchall()

        cursor.execute("SELECT ID_Modelo, Nome FROM Modelo ORDER BY Nome")
        modelos = cursor.fetchall()

    return render(request, 'admin_pecas_edit.html', {
        "peca_id": peca_id,
        "peca": peca,
        "marcas": marcas,
        "modelos": modelos
    })



# 🔹 Eliminar Peça
def admin_pecadelete(request, peca_id):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL delete_Peca(%s)", [peca_id])
            messages.success(request, "Peça eliminada com sucesso.")
        except DatabaseError as e:
            messages.error(request, "Erro ao eliminar a peça: " + str(e))

    return redirect("admin_pecaslist")

# 🔹 Listar Utilizadores

def admin_utilizadoreslist(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT U.ID_Utilizador, U.Nome, TU.Tipo, U.IsActive
            FROM Utilizador U
            JOIN TipoUtilizador TU ON U.ID_TipoUtilizador = TU.ID_TipoUtilizador
            ORDER BY U.Nome
        """)
        utilizadores = cursor.fetchall()

    return render(request, 'admin_utilizadores_list.html', {'utilizadores': utilizadores})

# 🔹 Criar Utilizador
def admin_utilizadorcreate(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        password = request.POST.get("password")
        id_tipo_utilizador = request.POST.get("id_tipo_utilizador")
        is_active = request.POST.get("is_active")

        # Converte o checkbox corretamente
        is_active = True if is_active == "on" else False

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL registar_Utilizador(%s, %s, %s, %s)", [nome, password, id_tipo_utilizador, is_active])
            return redirect('admin_utilizadoreslist')

        except Exception as e:
            error_message = "Erro ao criar o utilizador! Verifica os dados."
            return render(request, 'admin_utilizadores_create.html', {"error": error_message})

    # Buscar os tipos de utilizador para o dropdown
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_TipoUtilizador, Tipo FROM TipoUtilizador")
        tipos_utilizador = cursor.fetchall()

    return render(request, 'admin_utilizadores_create.html', {"tipos_utilizador": tipos_utilizador})

# 🔹 Editar Utilizador
def admin_utilizadoredit(request, utilizador_id):
    if request.method == "POST":
        nome = request.POST.get("nome")
        password = request.POST.get("password")
        id_tipo_utilizador = request.POST.get("id_tipo_utilizador")
        is_active = request.POST.get("is_active")

        is_active = True if is_active == "on" else False  

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL update_Utilizador(%s, %s, %s, %s, %s)", [utilizador_id, nome, password, is_active, id_tipo_utilizador])
            return redirect('admin_utilizadoreslist')
        except Exception as e:
            error_message = "Erro ao editar o utilizador!"
            return render(request, 'admin_utilizadores_edit.html', {
                "error": error_message,
                "utilizador_id": utilizador_id,
                "utilizador": (nome, password, is_active, id_tipo_utilizador)
            })

    with connection.cursor() as cursor:
        # Buscar os dados do utilizador
        cursor.execute("SELECT Nome, Password, IsActive, ID_TipoUtilizador FROM Utilizador WHERE ID_Utilizador = %s", [utilizador_id])
        utilizador = cursor.fetchone()

        # Buscar os tipos de utilizador
        cursor.execute("SELECT ID_TipoUtilizador, Tipo FROM TipoUtilizador")
        tipos_utilizador = cursor.fetchall()

    return render(request, 'admin_utilizadores_edit.html', {
        "utilizador_id": utilizador_id,
        "utilizador": utilizador,
        "tipos_utilizador": tipos_utilizador
    })


# 🔹 Eliminar Utilizador
def admin_utilizadordelete(request, utilizador_id):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL delete_Utilizador(%s)", [utilizador_id])
            return redirect('admin_utilizadoreslist')
        except Exception as e:
            print(f"Erro ao eliminar utilizador: {e}")
            return redirect('admin_utilizadoreslist')

    return redirect('admin_utilizadoreslist')

