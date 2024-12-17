from django.db import connections
import pymongo

# Executar o selecionar_TotalReservas para obter o numero total de reservas de um determinado utilizador
def getTotalReservasByUser(ID_user):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_TotalReservasByUser(%s);", (ID_user))
    users = cur.fetchone()  # Retorna um único registro (ou None)
    cur.close()  
    return users 






""" # Faz uma pesquisa a BD para obter todas as marcas presentes na BD
def getAllMarcas():
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM marca;")
    marcas = cur.fetchall()  # Retorna todos os registro (ou None)
    cur.close()  
    return marcas 

def deleteMarcaById(marcaid):
    with connections['default'].cursor() as cur:
        cur.execute("CALL deleteMarcaById(%s);", [marcaid])
 """