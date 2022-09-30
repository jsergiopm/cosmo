import PySimpleGUI as sg
import pandas as pd
import table_window



def create():
    move_files_window_layout =[
            [
                sg.T("")
            ],
            [sg.Text('Mover archivos másivamente', justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
            [
                sg.Text("Seleccionar inventario: (Inventario descargado de HADES .xls) "), 
                sg.Input(), sg.FileBrowse(key="excel", file_types=(('HADES','*.xls'),('INVENTARIO','*.xlsx')), button_text="Seleccionar")
            ],
            [
                sg.Listbox(values=[], enable_events=True, size=(40, 10), key="OLD-FILENAMES-LIST", visible = False),
            ],
            [
            sg.Button("Cargar inventario", disabled=False), sg.Text("Cargando inventario, por favor espere...", key="-LOADING-", visible=False),
            ], 
            ]

    move_files_window = sg.Window('Cosmo | Mover archivos', move_files_window_layout, icon="./assets/favicon.ico")
    while True:
        event, values = move_files_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            move_files_window.Close()
            break
        move_files_window["-LOADING-"].update(visible=True)
        move_files_window["Cargar inventario"].update(disabled=True)
        sg.popup("Espere mientras se carga el inventario...", auto_close=True )
        excel = values["excel"]
        data_from_excel = pd.read_html(excel)
        excel_2 = data_from_excel[0]
        data_from_excel = excel_2.values.tolist()
        if event == "Cargar inventario":
            move_files_window.close()
            headings = [str(data_from_excel[0][x]) for x in range(len(data_from_excel[0]))]
            table_window.create(data_from_excel, headings)
