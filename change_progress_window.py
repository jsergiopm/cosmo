import PySimpleGUI as sg
import os


def create(file_list, folder, list_of_new_names):
    BAR_MAX =  len(file_list)
    change_progress_window_layout = [[sg.Text('Cambiando nombres...')],
        [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
        [sg.Cancel()]]

    change_progress_window = sg.Window('Cambiar nombre de los archivos', change_progress_window_layout)

    for i in range(len(file_list)):
        event = change_progress_window.read(timeout=10)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        source = os.path.join(folder,file_list[i])
        destination = os.path.join(folder,list_of_new_names[i])
        os.rename(source, destination)
        change_progress_window['-PROG-'].update(i+1)
    change_progress_window.close()

    sg.popup('Tarea completada con éxito')