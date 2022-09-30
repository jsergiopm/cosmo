import PySimpleGUI as sg
import os
import take_out_files_progress_window
import cosmo

def collapse(layout, key, visible):
    return sg.pin(sg.Column(layout, key=key, visible=visible))
    

def create():

    subfolder_section = [
        [sg.T('Ingresa aquí el nombre de la carpeta'),
        sg.I('', k='-SUBFOLDER-')]
    ]

    take_out_files_layout=[
        [sg.Text("Selecciona la carpeta donde se encuentran actualmente los archivos: "), 
        sg.Push(), sg.Input(), sg.FolderBrowse(key='-SOURCE-', button_text="Seleccionar")],
        [sg.Text("Selecciona la carpeta donde quedarán los archivos: "), 
        sg.Push(), sg.Input(key='-DESTINATION-'), sg.FolderBrowse(button_text="Seleccionar")],
        [
                [sg.Checkbox('Selecciona esta opción si quieres buscar dentro de una carpeta específica', enable_events=True, key="-OPEN SEC SUBFOLDER-CHECKBOX")]
        ],
        [
                [collapse(subfolder_section, '-SUBFOLDER SECTION-', visible=False)]
        ],
        [sg.Button("Volver al inicio"), sg.Push(), sg.Button("Sacar archivos")]
    ]

    take_out_files_window = sg.Window("Sacar archivos", take_out_files_layout, icon="./assets/favicon.ico")

    opened = True

    while True:
        event, values = take_out_files_window.read()
        if event == 'exit' or event == sg.WIN_CLOSED:
            break

        if event.startswith('-OPEN SEC'):
            opened = not opened
            take_out_files_window['-OPEN SEC SUBFOLDER-CHECKBOX'].update(opened)
            take_out_files_window['-SUBFOLDER SECTION-'].update(visible=opened)

        if event == 'Sacar archivos':
            src_path = values['-SOURCE-']
            dst_path = values['-DESTINATION-']
            files_qty = 0
            for root, dirs, files in os.walk(src_path):
                for name in files:
                    if name.endswith((".pdf", ".PDF")):
                        files_qty += 1

            if files_qty > 0:
                if opened:
                    subfolder = values["-SUBFOLDER-"]
                    take_out_files_progress_window.create(files_qty, src_path, dst_path, subfolder)
                else:take_out_files_progress_window.create(files_qty, src_path, dst_path)
            else:
                sg.popup('No existen archivos PDF en la carpeta seleccionada')
        
        if event == 'Volver al inicio':
            take_out_files_window.close()
            cosmo.run()
