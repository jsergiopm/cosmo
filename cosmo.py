from cgitb import text
from re import T
import PySimpleGUI as sg
import csv
import shutil
import os
from datetime import datetime
import pandas as pd
from openpyxl import *



def read_csv(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        #next(reader, None)
        old_name_list = []
        new_name_list = []
        for row in reader:
            i = 0
            parts = row[i].split(";")
            old_name_list.append(parts[0] + ".pdf")
            new_name_list.append(parts[1] + ".pdf")
            i += 1 
        return old_name_list, new_name_list


def change_filename(list_of_files, old_names, new_names):
    new_list = []
    for file in list_of_files:
        try:
            index = old_names.index(file)
            new_list.append(new_names[index])
        except:
            pass
    return new_list


def run():
    #file_name, folder_name, status = read_csv()
    #move_file(file_name, folder_name, status)
    sg.theme("LightBrown3")

    layout = [
        [
            sg.T("")
        ],
        [sg.Text('Bienvenido a Cosmo', size=(30, 1), justification='center', font=("Helvetica", 25))],
        [sg.Text('Selecciona la instrucción que vas a ejecutar')], 
        [
        sg.Button("Cambiar"),
        sg.Button("Mover archivos"),
        ],  
    ]

    main_window = sg.Window('Cosmo', layout, size=(330,150))
    #window["OLD-FILENAMES-LIST"].hide()


    while True:
        event, values = main_window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            break
        elif event == "Cambiar":

            main_window.Close()
            layout2 = [
            [
                sg.T("")
            ],
            [sg.Text('Cambiar nombre de archivos másivamente', justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
            [
                [sg.Text("Selecciona una carpeta: "), 
                sg.FolderBrowse(key="FolderBrowse", button_text="Buscar")]
            ],
            [
                sg.Text("Seleccionar inventario: "), 
                sg.Input(), sg.FileBrowse(key="-FILE-", file_types=(('CSV FILES', '*.csv'),), button_text="Seleccionar")
            ],
            [
                sg.Listbox(values=[], enable_events=True, size=(40, 10), key="OLD-FILENAMES-LIST", visible = False),
                sg.Listbox(values=[], enable_events=True, size=(40, 10), key="NEW-FILENAMES-LIST",  visible = False)
            ],
            [
            sg.Button("Ver"),
            sg.Button("Comenzar")
            ], 
            ]
            
            change_filenames_window = sg.Window('Cosmo | Cambiar nombre', layout2)
            while True:
                event2, values2 = change_filenames_window.read()
                    
                if event2 == sg.WIN_CLOSED or event2 == 'Exit':
                    change_filenames_window.Close()
                    break
                folder = values2["FolderBrowse"]
                try:
                    # Get list of files in folder
                    file_list = os.listdir(folder)
                except:
                    file_list = []

                fnames = [
                    f
                    for f in file_list
                    if os.path.isfile(os.path.join(folder, f))
                    and f.lower().endswith((".pdf"))
                ]

                if event2 == "Ver":
                    change_filenames_window["OLD-FILENAMES-LIST"].update(visible=True)
                    change_filenames_window["NEW-FILENAMES-LIST"].update(visible=True)
                    change_filenames_window["OLD-FILENAMES-LIST"].update(fnames)
                    csv_file = values2["-FILE-"]
                    old_names, new_names = read_csv(csv_file)
                    list_of_new_names = change_filename(file_list, old_names, new_names)
                    change_filenames_window["NEW-FILENAMES-LIST"].update(list_of_new_names)
                if event2 == "Comenzar":
                    change_filenames_window.close()
                    BAR_MAX =  len(file_list)
                    layout3 = [[sg.Text('Cambiando nombres...')],
                        [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
                        [sg.Cancel()]]

                    change_progress_window = sg.Window('Cambiar nombre de los atchivos', layout3)

                    for i in range(len(file_list)):
                        event = change_progress_window.read(timeout=10)
                        if event == 'Cancel' or event == sg.WIN_CLOSED:
                            break
                        source = os.path.join(folder,file_list[i])
                        destination = os.path.join(folder,list_of_new_names[i])
                        os.rename(source, destination)
                        change_progress_window['-PROG-'].update(i+1)
                    change_progress_window.close()

                    sg.popup('Tarea completada con éxito')

        elif event == "Mover archivos":
            main_window.close()
            layout4 =[
            [
                sg.T("")
            ],
            [sg.Text('Mover archivos másivamente', justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
            [
                sg.Text("Seleccionar inventario: "), 
                sg.Input(), sg.FileBrowse(key="excel", file_types=(('XLSX FILES','*.xlsx'),('XLS FILES','*.xls')), button_text="Seleccionar")
            ],
            [
                sg.Listbox(values=[], enable_events=True, size=(40, 10), key="OLD-FILENAMES-LIST", visible = False),
            ],
            [
            sg.Button("Cargar inventario")
            ], 
            ]

            move_files_window = sg.Window('Cosmo | Mover archivos', layout4)
            while True:
                event4, values4 = move_files_window.read()
                if event4 == sg.WIN_CLOSED or event4 == 'Exit':
                    move_files_window.Close()
                    break
                excel = values4["excel"]
                data_from_excel = pd.read_html(excel)
                excel_2 = data_from_excel[0]
                data_from_excel = excel_2.values.tolist()
                # print(data_from_excel)
                if event4 == "Cargar inventario":
                    move_files_window.close()
                    headings = [str(data_from_excel[0][x])+' ..' for x in range(len(data_from_excel[0]))]
                    layout5 = [
                        [sg.Text('Cambiar nombre de archivos másivamente', justification='center')],
                        [sg.Table(values=data_from_excel, 
                        headings=headings, 
                        max_col_width=35,
                        auto_size_columns=True,
                        display_row_numbers=True,
                        justification='right',
                        num_rows=10,
                        key='-TABLE-',
                        row_height=35)]
                    ]

                    table_window = sg.Window("Información del inventario", layout5)
                    while True:
                        event5, values = table_window.read()
                        if event5 == "Exit" or event == sg.WIN_CLOSED:
                            break
                        table_window.close()
                            




if __name__ == "__main__":
    run()