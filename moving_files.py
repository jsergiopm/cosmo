import PySimpleGUI as sg
import os

def create(selected_column, src_path, dst_path):
    filenames =  os.listdir(src_path)
    BAR_MAX =  len(filenames)
    move_files_progress_window_layout = [[sg.Text('Moviendo ...')],
        [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
        [sg.Button('Cancelar')]]