from django.db import connections
import pymongo

# Executar o selecionar_UtilizadorByUsernameAndPassword para obter o id, nome e tipo de utilizador
def getUserByUsernameAndPassword(username, password):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_UtilizadorByUsernameAndPassword(%s, %s);", (username, password))
    users = cur.fetchone()  # Retorna um único registro (ou None)
    cur.close()  
    return users 

# Testes ......................................
def get_user_by_username_and_password2(username, password):
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_Utilizador(%s, %s);", (username, password))
    rows = cur.fetchone()  # Retorna um único registro (ou None)
    cur.close()  
    cur = connections['default'].cursor()
    cur.execute("SELECT * FROM selecionar_tipoutilizador(%s);", (rows.tipoUtilizador))
    rows = cur.fetchone()  # Retorna um único registro (ou None)
    cur.close() 
    users = [
        {
            "ID_Utilizador": row[0],
            "Nome": row[1],
            "Tipo": row[2],
        }
        for row in rows
    ]
    return users 
# Testes fim ......................................
