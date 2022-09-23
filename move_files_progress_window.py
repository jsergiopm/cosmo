import PySimpleGUI as sg
import os
import shutil
from pathlib import Path

def extract_id(filename):
    filename = filename.removesuffix('.pdf')
    filename = filename.removesuffix('.PDF')
    id = filename.split('-')
    id = id[0]
    return id

def create(src_path, dst_path, subfolder, filenames, headings, data_from_excel):
    files = os.listdir(src_path)
    BAR_MAX =  len(filenames) + len(files)

    move_files_progress_window_layout = [[sg.Text('Creando carpetas...', key='-STATUS-')],
        [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
        [sg.Button('Cancelar')]]
    

    move_files_progress_window = sg.Window('Crear carpetas', move_files_progress_window_layout)
 
    #Loop for create folder if no exists
    for i in range(len(filenames)):
        event, values = move_files_progress_window.read(10)
        if event == 'Cancelar' or event == sg.WIN_CLOSED:break
        destination = os.path.join(dst_path, filenames[i])
        if subfolder != 'none':destination = os.path.join(destination, subfolder)
        Path(destination).mkdir(parents= True, exist_ok= True)
        move_files_progress_window['-PROG-'].update(i+1)

    ids_in_inventory = []

    for row in range(len(data_from_excel)):
        if row > 0:
            ids_in_inventory.append(data_from_excel[row][7])

    unknown_elements = []

    for file in files:
        if file.endswith('.pdf') or file.endswith('PDF'):
            id = extract_id(file)
            try:
                index = ids_in_inventory.index(id)
                file_src = os.path.join(src_path, file)
                folder_dst = os.path.join(dst_path, filenames[index])
                file_dst = os.path.join(folder_dst, file)
                shutil.copy2(file_src, file_dst)
            except:
                unknown_elements.append(id)
            
    if len(unknown_elements) > 0:
        sg.popup("Existen elementos en la carpeta que no están en el inventario", unknown_elements)
            
    if i + 1 < len(filenames):
        sg.popup('Operación cancelada')
    else:
        sg.popup('Carpetas creadas con éxito')
            


