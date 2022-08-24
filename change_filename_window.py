import PySimpleGUI as sg
import csv
import os
import change_progress_window


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


def create():
    change_filenames_window_layout = [
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
    
    change_filenames_window = sg.Window('Cosmo | Cambiar nombre', change_filenames_window_layout)
    
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
            change_progress_window.create(file_list, folder, list_of_new_names)