import PySimpleGUI as sg
import os
import moving_files
from pathlib import Path


def create(src_path, dst_path, subfolder, filenames, headers):
    BAR_MAX =  len(filenames)
    move_files_progress_window_layout = [[sg.Text('Creando carpetas...')],
        [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
        [sg.Button('Cancelar')]]
    
    choose_filename_references_layout = [[sg.Text('Selecciona la columna del inventario que hace referencia al nombre del archivo')],
        [sg.Combo(headers, default_value="N° Identificacion", key='-Combo-')],
        [sg.Button('Mover archivos a carpetas', key='-NEXT-')]
    ]

    move_files_progress_window = sg.Window('Crear carpetas', move_files_progress_window_layout)

    for i in range(len(filenames)):
        event, values = move_files_progress_window.read(10)
        if event == 'Cancelar' or event == sg.WIN_CLOSED:break
        destination = os.path.join(dst_path, filenames[i])
        if subfolder != 'none':
            destination = os.path.join(destination, subfolder)
        Path(destination).mkdir(parents= True, exist_ok= True)
        move_files_progress_window['-PROG-'].update(i+1)
    if i + 1 < len(filenames):
        sg.popup('Operación cancelada')
    else:
        sg.popup('Carpetas creadas con éxito')
        choose_filename_references = sg.Window('Mover archivos', choose_filename_references_layout)
        while True:
            event, values = choose_filename_references.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                choose_filename_references.Close()
                break
            if event == "-NEXT-":
                selected_column = values['-COMBO-']
                choose_filename_references.close()
                moving_files.create(selected_column, src_path, dst_path)
