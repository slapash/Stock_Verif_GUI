
import pyodbc
from read_excel import isbn_file_read as fr
import pandas as pd
import sqlite3


#file = r"C:\Users\benai\Desktop\GLOVO.xlsx"

'DRIVER={SQL SERVER};SERVER={MOSQSDESKTOP\CDL_API_EXP};DATABASE={CARREFOURDULIVRE};Trust_Connection = yes;'
liste_en_stock = []
def demande(demande):

    driver_name = "SQL SERVER"
    server_name = "MOSQSDESKTOP\CDL_API_EXP"
    database_name = "CARREFOURDULIVRE"

    connect = sqlite3.connect('config.db')
    curseur = connect.cursor()
    curseur.execute('SELECT * FROM conf')
    infos = curseur.fetchall()
    for elem1, elem2, elem3 in infos:
        driver_name = elem1
        server_name = elem2
        database_name = elem3


    connection_string = f"""
    DRIVER={{{driver_name}}};
    SERVER={{{server_name}}};
    DATABASE={{{database_name}}};
    Trust_Connection = yes;
"""

    global liste_en_stock
    cnxn = pyodbc.connect(connection_string)
    
    cursor = cnxn.cursor()

    #cursor.execute(f"SELECT COUNT(*) from v_ART_EnStock WHERE ARTCB = '{demande}'")
    cursor.execute(f"""SELECT ARTCB, ARTTIT1, ARTTIT2, STKQTEREEL
                    FROM ART INNER JOIN STK
                    ON(ART.ARTCOD = STK.ARTCOD)
                    WHERE ARTCB IN {demande}
""")
  
    for row in cursor:
        liste_en_stock.append(row)

    cursor.close()
    cnxn.close()
    
    return liste_en_stock
#dev (works  outputs list of tuples)


