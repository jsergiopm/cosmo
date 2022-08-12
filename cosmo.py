from re import T
import PySimpleGUI as sg
import csv
import shutil
import os
from datetime import datetime


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

def write_log(message):
    f = open("log.txt", "a")
    current_datetime = datetime.now()
    f.write(str(current_datetime) + '\n' + message)
    f.close()


def find_item(HL, item):
    for i in range(len(HL)):
        if HL[i] == item: 
            return i 


def iterative_file_name(file):
    if file.find("-") != -1:
        if file.find("-1") != -1:
            file = file.replace("-1", "-2")
        elif file.find("-2") != -1:
            file = file.replace("-2", "-3")
        elif file.find("-3") != -1:
            file = file.replace("-3", "-4")
        elif file.find("-4") != -1:
            file = file.replace("-4", "-5")
        elif file.find("-5") != -1:
            file = file.replace("-5", "-6")
    else:
        file = file.replace(".pdf", "-1.pdf")
    return file


def move_file(file_name, folder_names, status):
    log = ""
    only_files = next(os.walk('D:/Activos/Prestaciones_recuperadas/'))[2] 
    none_list = []
    for file in only_files:
        file_without_index = file.replace("PDF", "pdf")
        file = file.replace("PDF", "pdf")
        file_without_index = file.replace("-1", "")
        file_without_index = file_without_index.replace("-2", "")
        file_without_index = file_without_index.replace("-3", "")
        file_without_index = file_without_index.replace("-4", "")
        file_without_index = file_without_index.replace("-5", "")
        #source = 'C:/Users/Tesoreria/Desktop/Prueba/origen/' + file
        source = 'D:/Activos/Prestaciones_recuperadas/' + file
        index = find_item(file_name, file_without_index)
        if index == None:
            none_list.append(file)
            continue
        if status[index].strip() == "ACTIVOS":
            destination = 'D:/CARPETAS/ACTIVOS/' + folder_names[index] + '/PrestacionSocial/' + file
        elif status[index] == "INACTIVOS":
            destination = 'D:/CARPETAS/INACTIVOS/' + folder_names[index] + '/PrestacionSocial/' + file
        if os.path.exists(destination):
            file = iterative_file_name(file)
            print("El archivo ya se encuentra en el destino, el nombre del archivo ahora es", file)
            #log += "El archivo "+ file + " ya se encuentra en el destino \n"
            #continue
        try:
            shutil.move(source, destination)
        except FileNotFoundError:
            print('El archivo', file, 'no fue encontrado, revise la ruta')
            log += 'El archivo ' + file + ' no fue encontrado, revise la ruta\n'
            continue
        print("Moved: " + file)
        log += "Moved: " + file + "\n"
    if none_list != []:
        print(len(none_list) , "elementos no fueron encontrados en el inventario: ")
        print(none_list)
    log += str(len(none_list)) + " elementos no fueron encontrados en el inventario: \n"
    for none_item in none_list:
        log += none_item 
        log += "\n"
    write_log(log + '\n')


def change_filename(list_of_files, old_names, new_names):
    new_list = []
    for file in list_of_files:
        index = old_names.index(file)
        new_list.append(new_names[index])
    print(new_list)


def run():
    #file_name, folder_name, status = read_csv()
    #move_file(file_name, folder_name, status)
    sg.theme("LightBrown3")

    layout = [[
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
    #window["-FILE LIST-"].hide()

    window2_active = False
    while True:
        event, values = main_window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            break
        elif event == "Cambiar":
            window_2_active = True
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
                sg.Input(), sg.FileBrowse(key="-FILE-", file_types=(('CSV FILES'), ('*.csv')), button_text="Seleccionar")
            ],
            [
                sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")
            ],
            [
            sg.Button("Ver"),
            sg.Button("Comenzar")
            ], 
            ]
            
            change_window = sg.Window('Cosmo | Cambiar nombre', layout2)
            while True:
                event2, values2 = change_window.read()
                    
                if event2 == sg.WIN_CLOSED or event2 == 'Exit':
                    change_window.Close()
                    window_2_active = False
                    #main_window.UnHide()
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
                change_window["-FILE LIST-"].update(fnames)
                if event2 == "Comenzar":
                    csv_file = values2["-FILE-"]
                    old_names, new_names = read_csv(csv_file)


if __name__ == "__main__":
    run()