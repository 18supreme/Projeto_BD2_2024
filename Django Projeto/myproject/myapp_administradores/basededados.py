from django.db import connections
import pymongo

# Faz uma pesquisa a BD para obter todas as marcas presentes na BD
def getAllMarcas():
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM marca;")
    marcas = cur.fetchall()  # Retorna todos os registro (ou None)
    cur.close()  
    return marcas 

# Elimina da BD a Marca com o Id fornecido
def deleteMarcaById(marcaid):
    with connections['default'].cursor() as cur:
        cur.execute("CALL deleteMarcaById(%s);", [marcaid])
