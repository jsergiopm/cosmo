from distutils.log import error
from hashlib import new
import PySimpleGUI as sg
import os
import shutil
from pathlib import Path
import cosmo


def extract_id(filename):
    filename = filename.removesuffix('.pdf')
    filename = filename.removesuffix('.PDF')
    id = filename.split('-')
    id = id[0]
    return id

def add_iterator(file):
    file = file.replace('.pdf', '-1.pdf')
    i = 1
    j = 0
    while os.path.exists(file):
        i += 1
        j += 1
        old_name = '-%i.pdf' % (j)
        new_name = '-%i.pdf' % (i)
        file = file.replace(old_name, new_name)
    return file

def create(src_path, dst_path, subfolder, filenames, data_from_excel, column):
    files = os.listdir(src_path)
    BAR_MAX =  len(filenames) + len(files)

    move_files_progress_window_layout = [[sg.Text('Creando carpetas...', key='-STATUS-')],
        [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
        [sg.Button('Cancelar')]]
    
    not_moved_or_not_created_layout = [

    ]
    

    move_files_progress_window = sg.Window('Crear carpetas', move_files_progress_window_layout, icon="./assets/favicon.ico")
    
    error_folders = []

    #Loop for create folder if no exists
    for i in range(len(filenames)):
        event, values = move_files_progress_window.read(10)
        if event == 'Cancelar' or event == sg.WIN_CLOSED:break
        destination = os.path.join(dst_path, filenames[i])
        if subfolder != 'none':destination = os.path.join(destination, subfolder)
        try:
            Path(destination).mkdir(parents= True, exist_ok= True)
        except:
            error_folders.append(filenames[i])
        move_files_progress_window['-PROG-'].update(i+1)

    ids_in_inventory = []

    for row in range(len(data_from_excel)):
        if row > 0:
            ids_in_inventory.append(data_from_excel[row][column])

    unknown_elements = []

    for file in files:
        if file.endswith('.pdf') or file.endswith('PDF'):
            id = extract_id(file)
            try:
                index = ids_in_inventory.index(id)
                file_src = os.path.join(src_path, file)
                folder_dst = os.path.join(dst_path, filenames[index])
                file_dst = os.path.join(folder_dst, file)
                if os.path.exists(file_dst):file_dst = add_iterator(file_dst)
                shutil.copy2(file_src, file_dst)
            except:
                unknown_elements.append(id)
            
    if (len(unknown_elements) > 0) or (len(error_folders) > 0):
        if len(unknown_elements) > 0:
            print("Existen elementos", len(unknown_elements),"en la carpeta que no están en el inventario")
            print("Existen elementos en la carpeta que no están en el inventario", unknown_elements)
        if len(error_folders) > 0:
            print("Existen carpetas que no se crearon por problemas en sus nombres", error_folders)
            
    if i + 1 < len(filenames):
        sg.popup('Operación cancelada')
    else:
        move_files_progress_window.close()
        sg.popup('Carpetas nuevas creadas y archivos copiados con éxito')
        cosmo.run()
            


