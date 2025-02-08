from django.db import connections
import pymongo

# Executar o selecionar_TotalReservas para obter o numero total de reservas de um determinado utilizador
def getTotalReservasByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_ReservaByUser(%s);", (ID_user,))
    total_reservas = cur.fetchone()[0] # Retorna um único registro (ou None)
    cur.close()  
    return total_reservas 

# Executar o selecionar_PercentDanos para obter a percentagem de danos de um determinado utilizador
def getDanosByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_PercentDanosByUser(%s);", (ID_user,))
    percentagem_danos = cur.fetchone()[0] # Retorna um único registro (ou None)
    cur.close()  
    return percentagem_danos 

# Executar o selecionar_MarcaByUser para obter a marca mais usada de um determinado utilizador
def getMarcaFavoritaByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_MarcaByUser(%s);", (ID_user,))
    marca_preferida = cur.fetchone() # Retorna um único registro (ou None)
    cur.close()  
    return marca_preferida 

# Executar o selecionar_ModeloByUser para obter o modelo mais usado de um determinado utilizador
def getModeloFavoritaByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_ModeloByUser(%s);", (ID_user,))
    modelo_preferido = cur.fetchone() # Retorna um único registro (ou None)
    cur.close()  
    return modelo_preferido 

# Executar o selecionar_MediaKmByUser para obter a média de KM realizados por um determinado utilizador
def getMedKmByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_MediaKmByUser(%s);", (ID_user,))
    MédiaKmPercorridos = cur.fetchone()[0] # Retorna um único registro (ou None)
    cur.close()  
    return MédiaKmPercorridos 

# Executar o selecionar_MediaKmByUser para obter o total dos KM realizados por um determinado utilizador
def getTotalKmByUser(ID_user):
    with connections['default'].cursor() as cur:
        cur.execute("SELECT * FROM selecionar_TotalKmByUser(%s);", (ID_user,))
        result = cur.fetchone()
        return f"{result[0]:,.2f} KM" if result else "0.00 KM"  # Formatação correta
 
 # Executar o selecionar_Top3Viaturas para obter as 3 viaturas mais requisitadas
def getTop3Viaturas():
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_gettop3Viaturas();")
    viaturas_tendencias = cur.fetchall() # Uso do fetchall() para obter as 3 viaturas
    cur.close()  
    return viaturas_tendencias 

 # Executar o selecionar_Viaturas para obter todas as viaturas
def getViaturas():
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_viaturas();")
    viaturas = cur.fetchall() 
    cur.close()  
    return viaturas 


 # Executar o selecionar_DetailViaturaById para obter os detalhes de uma determinada viatura
def getDetailViaturaById(ID_viat):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_DetailViaturaById(%s);", (ID_viat,))
    viatura = cur.fetchone() 
    cur.close()  
    return viatura

 # Executar o selecionar_ReservaByUser para obter as reservas para a listagem 
def getListReservaById(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_ReservaByUser(%s);", (ID_user,))
    reservas = cur.fetchall() 
    cur.close()  
    return reservas

 # Executar o selecionar_conflitoReserva para conferir se a reserva já existe
def getconflitoReserva(viatura_id, data_inicio, data_fim):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_conflitoReserva(%s,%s,%s);", (viatura_id, data_inicio, data_fim,))
    conflito = cur.fetchone()[0]
    cur.close()  
    return conflito

# Elimina da BD a Marca com o Id fornecido
def CreateNewReserva(Data_Inicio, Data_Fim, Danos, DanosTexto, KMPercorridos, ID_Viatura, ID_Utilizador, ID_EstadoReserva):
    with connections['default'].cursor() as cur:
        cur.execute("CALL registar_Reserva(%s, %s, %s, %s, %s, %s, %s, %s);", (Data_Inicio, Data_Fim, Danos, DanosTexto, KMPercorridos, ID_Viatura, ID_Utilizador, ID_EstadoReserva,))


# Atualiza o estado da reserva
def UpdateReserva(reserva_id, ID_EstadoReserva):
    with connections['default'].cursor() as cur:
        cur.execute("CALL update_Reserva(%s, %s);", (reserva_id, ID_EstadoReserva))
        if (ID_EstadoReserva == 5 or ID_EstadoReserva == 4):
            UpdateEstadoViaturaReserva(reserva_id, 1)

def UpdateEstadoViaturaReserva(reserva_id, id_estadoviatura):
    with connections['default'].cursor() as cursor:
        # Obter o ID da viatura associada à reserva
        cursor.execute("SELECT ID_Viatura FROM Reserva WHERE id_reserva = %s", [reserva_id])
        viatura_id = cursor.fetchone()[0]

        # Atualizar o estado da viatura para "Alugado" (id_estadoviatura = 1)
        cursor.execute("""
            UPDATE Viatura
            SET id_Estado_Viatura = %s
            WHERE ID_Viatura = %s;
        """, [id_estadoviatura, viatura_id])






""" # Exemplo de Função 
def getAllMarcas():
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM marca;")
    marcas = cur.fetchall()  # Retorna todos os registro (ou None)
    cur.close()  
    return marcas 

# Exemplo de Procedimento
def deleteMarcaById(marcaid):
    with connections['default'].cursor() as cur:
        cur.execute("CALL deleteMarcaById(%s);", [marcaid]) """
