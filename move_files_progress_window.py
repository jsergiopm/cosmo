from genericpath import exists
import PySimpleGUI as sg
import os
from pathlib import Path


def create(src_path, dst_path, subfolder, filenames):
    BAR_MAX =  len(filenames)
    move_files_progress_window_layout = [[sg.Text('Creando carpetas...')],
        [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
        [sg.Button('Cancelar')]]

    move_files_progress_window = sg.Window('Crear carpetas', move_files_progress_window_layout)

    for i in range(len(filenames)):
        event, values = move_files_progress_window.read(10)
        if event == 'Cancelar' or event == sg.WIN_CLOSED:break
        destination = os.path.join(dst_path, filenames[i])
        if subfolder != 'none':
            destination = os.path.join(destination, subfolder)
        Path(destination).mkdir(parents= True, exist_ok= True)
        move_files_progress_window['-PROG-'].update(i+1)
    # move_files_progress_window.close()
    if i + 1 < len(filenames):
        sg.popup('Operación cancelada')
    else:
        sg.popup('Carpetas creadas con éxito')