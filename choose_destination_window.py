import PySimpleGUI as sg


def create():
    choose_destination_window_layout = [
        [
                [sg.Text("Selecciona la carpeta de origen: "), 
                sg.FolderBrowse(key="SourceFolderBrowse", button_text="Buscar")]
        ],
        [
                [sg.Text("Selecciona la carpeta de destino: "), 
                sg.FolderBrowse(key="DestinationFolderBrowse", button_text="Buscar")]
        ],
                [sg.Push(), sg.Button('Convertir'), sg.Push()]
        ]

    choose_destination_window = sg.Window('Mover archivos', choose_destination_window_layout)
    while True:
        event, values = choose_destination_window.read()
        if event == sg.WIN_CLOSED():
            break