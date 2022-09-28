import PySimpleGUI as sg
import os
import shutil
from pathlib import Path

def create(qty, src_path, dst_path, subfolder):
    BAR_MAX = qty
    take_out_files_progress_window_layout = [[sg.Text('Sacando archivos...')],
    [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
    [sg.Cancel()]]

    pdf_count = 0

    take_out_files_progress_window = sg.Window('Sacando los archivos', take_out_files_progress_window_layout, icon="./assets/favicon.ico")
    files_qty = 0
    for root, dirs, files in os.walk(src_path):
        event = take_out_files_progress_window.read(timeout=10)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        for name in files:
            if subfolder != "":
                if name.endswith((".pdf", ".PDF")):
                    files_qty += 1
                    src_root = Path(root)
                    src_file_path = src_root.joinpath(name)
                    parent = os.path.basename(os.path.dirname(src_file_path))
                    if parent == subfolder:
                        dst_root = Path(dst_path)
                        dst_file_path = dst_root.joinpath(name)
                        shutil.copyfile(src_file_path, dst_file_path)
                        pdf_count += 1
                        take_out_files_progress_window['-PROG-'].update(files_qty)
    
    sg.popup("La cantidad de PDF's es ", pdf_count)
    take_out_files_progress_window.Close()

    sg.popup('Tarea completada con éxito')

