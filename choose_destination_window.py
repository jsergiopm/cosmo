from cgitb import enable
import PySimpleGUI as sg


def collapse(layout, key, visible):
    return sg.pin(sg.Column(layout, key=key, visible=visible))
    

def create():
    subfolder_section = [
        [sg.T('Ingresa aquí el nombre de la subcarpeta'),
        sg.I('', k='-SUBFOLDER-')]
    ] 

    choose_destination_window_layout = [
        [
                [sg.Text("Selecciona la carpeta donde se encuentran actualmente los archivos: "), 
                 sg.Push(), sg.Input(), sg.FolderBrowse(button_text="Seleccionar")]
        ],
        [
                [sg.Text("Selecciona la carpeta donde quedarán los archivos: "), 
                sg.Push(), sg.Input(), sg.FolderBrowse(button_text="Seleccionar")]
        ],
        [
                [sg.Checkbox('Añadir subcarpetas', enable_events=True, key="-OPEN SEC SUBFOLDER-CHECKBOX")]
        ],
        [
                [collapse(subfolder_section, '-SUBFOLDER SECTION-', visible=False)]
        ],
                [sg.Push(), sg.Button('Convertir'), sg.Push()]
        ]


    choose_destination_window = sg.Window('Mover archivos', choose_destination_window_layout)
    
    opened = True 

    while True:
        event, values = choose_destination_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break 
        
        if event.startswith('-OPEN SEC'):
            opened = not opened
            choose_destination_window['-OPEN SEC SUBFOLDER-CHECKBOX'].update(opened)
            choose_destination_window['-SUBFOLDER SECTION-'].update(visible=opened)
        

    choose_destination_window.close()