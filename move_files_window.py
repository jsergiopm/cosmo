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
                sg.Text("Seleccionar inventario: "), 
                sg.Input(), sg.FileBrowse(key="excel", file_types=(('HADES','*.xls'),('INVENTARIO','*.xlsx')), button_text="Seleccionar")
            ],
            [
                sg.Listbox(values=[], enable_events=True, size=(40, 10), key="OLD-FILENAMES-LIST", visible = False),
            ],
            [
            sg.Button("Cargar inventario")
            ], 
            ]

    move_files_window = sg.Window('Cosmo | Mover archivos', move_files_window_layout)
    while True:
        event, values = move_files_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            move_files_window.Close()
            break
        excel = values["excel"]
        data_from_excel = pd.read_html(excel)
        excel_2 = data_from_excel[0]
        data_from_excel = excel_2.values.tolist()
        # print(data_from_excel)
        if event == "Cargar inventario":
            move_files_window.close()
            headings = [str(data_from_excel[0][x]) for x in range(len(data_from_excel[0]))]
            table_window.create(data_from_excel, headings)