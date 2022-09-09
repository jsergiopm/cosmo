import PySimpleGUI as sg
import os
import take_out_files_progress_window


def create():
    take_out_files_layout=[
        [sg.Text("Selecciona la carpeta donde se encuentran actualmente los archivos: "), 
        sg.Push(), sg.Input(), sg.FolderBrowse(key='-SOURCE-', button_text="Seleccionar")],
        [sg.Text("Selecciona la carpeta donde quedarán los archivos: "), 
        sg.Push(), sg.Input(key='-DESTINATION-'), sg.FolderBrowse(button_text="Seleccionar")],
        [sg.Push(), sg.Button("Sacar archivos")]
    ]

    take_out_files_window = sg.Window("Sacar archivos", take_out_files_layout)

    while True:
        event, values = take_out_files_window.read()
        if event == 'exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Sacar archivos':
            src_path = values['-SOURCE-']
            dst_path = values['-DESTINATION-']
            files_qty = 0
            for root, dirs, files in os.walk(src_path):
                for name in files:
                    if name.endswith((".pdf", ".PDF")):
                        files_qty += 1

            if files_qty > 0:
                take_out_files_progress_window.create(files_qty, src_path, dst_path)
            else:
                sg.popup('No existen archivos PDF en la carpeta seleccionada')
