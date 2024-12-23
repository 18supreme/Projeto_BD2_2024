from django.db import connections
import pymongo

# Executar o selecionar_TotalReservas para obter o numero total de reservas de um determinado utilizador
def getTotalReservasByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_TotalReservasByUser(%s);", (ID_user))
    total_reservas = cur.fetchone()[0] # Retorna um único registro (ou None)
    cur.close()  
    return total_reservas 

# Executar o selecionar_PercentDanos para obter a percentagem de danos de um determinado utilizador
def getDanosByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_PercentDanosByUser(%s);", (ID_user))
    percentagem_danos = cur.fetchone()[0] # Retorna um único registro (ou None)
    cur.close()  
    return percentagem_danos 

# Executar o selecionar_MarcaByUser para obter a marca mais usada de um determinado utilizador
def getMarcaFavoritaByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_MarcaByUser(%s);", (ID_user))
    marca_preferida = cur.fetchone() # Retorna um único registro (ou None)
    cur.close()  
    return marca_preferida 

# Executar o selecionar_ModeloByUser para obter o modelo mais usado de um determinado utilizador
def getModeloFavoritaByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_ModeloByUser(%s);", (ID_user))
    modelo_preferido = cur.fetchone() # Retorna um único registro (ou None)
    cur.close()  
    return modelo_preferido 

# Executar o selecionar_MediaKmByUser para obter a média de KM realizados por um determinado utilizador
def getMedKmByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_MediaKmByUser(%s);", (ID_user))
    MédiaKmPercorridos = cur.fetchone()[0] # Retorna um único registro (ou None)
    cur.close()  
    return MédiaKmPercorridos 

# Executar o selecionar_MediaKmByUser para obter o total dos KM realizados por um determinado utilizador
def getTotalKmByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_TotalKmByUser(%s);", (ID_user))
    getTotalKmByUser = cur.fetchone()[0] # Retorna um único registro (ou None)
    cur.close()  
    return getTotalKmByUser 
 
 # Executar o selecionar_Top3Viaturas para obter as 3 viaturas mais requisitadas
def getTop3Viaturas():
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_Top3Viaturas();")
    viaturas_tendencias = cur.fetchall() # Uso do fetchall() para obter as 3 viaturas
    cur.close()  
    return viaturas_tendencias 

 # Executar o selecionar_Viaturas para obter todas as viaturas
def getViaturas():
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_Viaturas();")
    viaturas = cur.fetchall() 
    cur.close()  
    return viaturas 


 # Executar o selecionar_DetailViaturaById para obter os detalhes de uma determinada viatura
def getDetailViaturaById(ID_viat):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_DetailViaturaById(%s);", (ID_viat))
    viatura = cur.fetchone() 
    cur.close()  
    return viatura

 # Executar o selecionar_ReservaByUser para obter as reservas para a listagem 
def getListReservaById(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_ReservaByUser(%s);", (ID_user))
    reservas = cur.fetchall() 
    cur.close()  
    return reservas

 # Executar o selecionar_conflitoReserva para conferir se a reserva já existe
def getconflitoReserva(viatura_id, data_inicio, data_fim):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_conflitoReserva(%s,%s,%s);", (viatura_id, data_inicio, data_fim))
    conflito = cur.fetchone()[0]
    cur.close()  
    return conflito

# Elimina da BD a Marca com o Id fornecido
def CreateNewReserva(Data_Inicio, Data_Fim, Danos, DanosTexto, KMPercorridos, ID_Viatura, ID_Utilizador, ID_EstadoReserva):
    with connections['default'].cursor() as cur:
        cur.execute("CALL registar_Reserva(%s);", [Data_Inicio, Data_Fim, Danos, DanosTexto, KMPercorridos, ID_Viatura, ID_Utilizador, ID_EstadoReserva])

# Atualiza o estado da reserva
def UpdateReserva(reserva_id, ID_EstadoReserva):
    with connections['default'].cursor() as cur:
        cur.execute("CALL update_Reserva(%s, %s);", [reserva_id, ID_EstadoReserva])







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
