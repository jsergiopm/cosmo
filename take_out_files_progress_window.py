import PySimpleGUI as sg
import os
import shutil
from pathlib import Path

def create(qty, src_path, dst_path):
    BAR_MAX = qty
    take_out_files_progress_window_layout = [[sg.Text('Sacando archivos...')],
    [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
    [sg.Cancel()]]

    take_out_files_progress_window = sg.Window('Sacando los archivos', take_out_files_progress_window_layout, icon="./assets/favicon.ico")
    files_qty = 0
    for root, dirs, files in os.walk(src_path):
        event = take_out_files_progress_window.read(timeout=10)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        for name in files:
            if name.endswith((".pdf", ".PDF")):
                files_qty += 1
                src_root = Path(root)
                src_file_path = src_root.joinpath(name)
                dst_root = Path(dst_path)
                dst_file_path = dst_root.joinpath(name)
                shutil.copyfile(src_file_path, dst_file_path)
                take_out_files_progress_window['-PROG-'].update(files_qty)
    
    take_out_files_progress_window.close()

    sg.popup('Tarea completada con éxito')

