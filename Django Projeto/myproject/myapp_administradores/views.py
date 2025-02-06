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


def create_manutencao(request):
    if request.method == "POST":
        valor = request.POST.get("valor")
        descricao = request.POST.get("descricao")
        data = request.POST.get("data")
        viatura_id = request.POST.get("viatura")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Manutencao (Valor, Descricao, Data, ID_Viatura)
                VALUES (%s, %s, %s, %s)
                """, [valor, descricao, data, viatura_id]
            )

        return redirect('admin_manutencoes')  # Redireciona para a página de manutenções após criação
    
    # Se o método for GET, apenas mostra o formulário de criação
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Viatura, Matricula FROM Viatura")
        viaturas = cursor.fetchall()

    return render(request, "admin_manutencoes_create.html", {"viaturas": viaturas})


def edit_manutencao(request, manutencao_id):
    if request.method == "POST":
        valor = request.POST.get("valor")
        descricao = request.POST.get("descricao")
        data = request.POST.get("data")
        viatura_id = request.POST.get("viatura")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE Manutencao
                SET Valor = %s, Descricao = %s, Data = %s, ID_Viatura = %s
                WHERE ID_Manutencao = %s
                """, [valor, descricao, data, viatura_id, manutencao_id]
            )
        return JsonResponse({"success": True})

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Manutencao WHERE ID_Manutencao = %s", [manutencao_id])
        manutencao = cursor.fetchone()

        cursor.execute("SELECT ID_Viatura, Matricula FROM Viatura")
        viaturas = cursor.fetchall()

    return render(request, "manutencoes/edit.html", {"manutencao": manutencao, "viaturas": viaturas})


def delete_manutencao(request, manutencao_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Manutencao WHERE ID_Manutencao = %s", [manutencao_id])
    return JsonResponse({"success": True})


def admin_administracao(request):
    return render(request, 'admin_administracao.html')


# Lista de Marcas
def admin_marcaslist(request):
    with connection.cursor() as cursor:
        # Consulta SQL para obter as marcas
        cursor.execute("SELECT ID_Marca, Nome, IsActive FROM Marca")
        marcas = cursor.fetchall()

    context = {'marcas': marcas}
    return render(request, 'admin_marcaslist.html', context)

# Criar Marca
from django.shortcuts import render, redirect
from django.db import connection, DatabaseError

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



# Editar Marca
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



# Eliminar Marca
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

# Lista de Modelos
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

# Criar Modelo
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

# Editar Modelo
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

# Eliminar Modelo
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
