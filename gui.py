import PySimpleGUI as sg
from read_excel import isbn_file_read as fr
from DB_query import demande 
import sqlite3



config = []

def last(n):
    return n[-1]

def sort(tuples):
    return sorted(tuples, key = last)

def popup_config(window):
    layout2 = [
                [sg.T("entrez les informations sous le format DRIVER/NOM_SERVEUR/NOM_BASE_DONEE"), sg.Input()],
                [sg.Button("OK", key = "ok-popup")]
              ]
    

    win = sg.Window("My Popup", layout2, modal=True,
        grab_anywhere=True, enable_close_attempted_event=True)
    event, value = win.read()
    
    win.close()  
    window.write_event_value(event, value)

heading = ['ISBN', 'titre', 'titre2', 'stock']
rows = []

layout = [
            [sg.Text(key='infos')],
            [sg.Table(values = rows, headings=heading, auto_size_columns = False, def_col_width = 1, max_col_width=100 , justification= "left", expand_x = True, expand_y = True, border_width=1, key = '-TABLE-')],
            [sg.Button('configurer'), sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse('ajouter un fichier',  file_types=(("Excel files", "*.xlsx"),)), sg.Button('OK')]
         ]



window = sg.Window("Stock Verif", layout, size = (1024,768), resizable = True)


while True:
    event, values = window.read()
    if event == 'OK':
        resultat = demande(fr(values["-FILE-"]))
        resultat = sort(resultat)
        
        for elem1, elem2, elem3, elem4 in resultat:
            elem4 = int(elem4)
            rows.append([elem1,elem2,elem3,elem4])
        window['-TABLE-'].update(values=rows)
    
    if event == 'configurer':
        popup_config(window)

    if event == "ok-popup":
        connect = sqlite3.connect('config.db')
        curseur = connect.cursor()

        config_values = values[event][0].split('/')
        with connect:
                    curseur.execute("UPDATE conf Set driver = :DRIVER, server_name = :SVR_NAME, database_name = :DB_NAME  ", {'DRIVER': config_values[0], 'SVR_NAME': config_values[1], 'DB_NAME': config_values[2] })
        
        for row in curseur:
            config_values = row
            break
        window['infos'].update(config_values)
        
    if event == sg.WIN_CLOSED:
        break

    
    
window.close()


