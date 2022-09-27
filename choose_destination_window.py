from pathlib import Path
import PySimpleGUI as sg
import choose_move_files_options_window


def collapse(layout, key, visible):
    return sg.pin(sg.Column(layout, key=key, visible=visible))
    

def create(data_from_excel, headings):
    subfolder_section = [
        [sg.T('Ingresa aquí el nombre de la subcarpeta'),
        sg.I('', k='-SUBFOLDER-')]
    ] 

    choose_destination_window_layout = [
        [
                [sg.Text("Selecciona la carpeta donde se encuentran actualmente los archivos: "), 
                 sg.Push(), sg.Input(), sg.FolderBrowse(key="-SRC FOLDER-", button_text="Seleccionar")]
        ],
        [
                [sg.Text("Selecciona la carpeta donde quedarán los archivos: "), 
                sg.Push(), sg.Input(), sg.FolderBrowse(key="-DST FOLDER-", button_text="Seleccionar")]
        ],
        [
                [sg.Checkbox('Añadir subcarpeta', enable_events=True, key="-OPEN SEC SUBFOLDER-CHECKBOX")]
        ],
        [
                [collapse(subfolder_section, '-SUBFOLDER SECTION-', visible=False)]
        ],
                [ sg.Button('Siguiente')]
        ]


    choose_destination_window = sg.Window('Mover archivos', choose_destination_window_layout, icon="./assets/favicon.ico")
    
    opened = True 

    while True:
        event, values = choose_destination_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break 
        
        if event.startswith('-OPEN SEC'):
            opened = not opened
            choose_destination_window['-OPEN SEC SUBFOLDER-CHECKBOX'].update(opened)
            choose_destination_window['-SUBFOLDER SECTION-'].update(visible=opened)


        if event == "Siguiente":
            source_folder = values["-SRC FOLDER-"]
            source_path = Path(source_folder)
            destination_folder = values["-DST FOLDER-"]
            destination_path = Path(destination_folder)
            if opened:
                subfolder = values["-SUBFOLDER-"]
                choose_destination_window.close()
                choose_move_files_options_window.create(data_from_excel, headings, source_path, destination_path, subfolder)
            else:
                choose_destination_window.close()
                choose_move_files_options_window.create(data_from_excel, headings, source_path, destination_path, "none")
