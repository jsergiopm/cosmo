import PySimpleGUI as sg
import os

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

def change_filename(file, old_names, new_names):
    try:return new_names[old_names.index(file)]
    except:return ""


def create(old_names, new_names, folder, file_list):
    BAR_MAX =  len(file_list)
    change_progress_window_layout = [[sg.Text('Cambiando nombres...')],
        [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
        [sg.Cancel()]]

    change_progress_window = sg.Window('Cambiar nombre de los archivos', change_progress_window_layout, icon="./assets/favicon.ico")

    for i in range(len(file_list)):
        event = change_progress_window.read(timeout=10)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        source = os.path.join(folder, file_list[i])
        file = file_list[i].replace(".PDF",".pdf")
        file = change_filename(file, old_names, new_names)
        destination = os.path.join(folder, file)
        if file != "":
            if os.path.exists(destination):destination = add_iterator(destination)
            os.rename(source, destination)
        change_progress_window['-PROG-'].update(i+1)
    change_progress_window.close()

    sg.popup('Tarea completada con éxito')