import PySimpleGUI as sg
import os


def create(src_path, dst_path, subfolder, filenames):
    BAR_MAX =  len(filenames)
    move_files_progress_window_layout = [[sg.Text('Creando carpetas...')],
        [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
        [sg.Cancel()]]

    move_files_progress_window = sg.Window('Cambiar nombre de los archivos', move_files_progress_window_layout)

    for i in range(len(filenames)):
        event = move_files_progress_window.read(timeout=10)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        source = os.path.join(src_path,filenames[i])
        destination = os.path.join(folder,list_of_new_names[i])
        os.rename(source, destination)
        move_files_progress_window['-PROG-'].update(i+1)
    move_files_progress_window.close()

    sg.popup('Tarea completada con éxito')