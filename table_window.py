import PySimpleGUI as sg

def create(data_from_excel, headings):
    table_window_layout = [
                        [sg.Text('Cambiar nombre de archivos másivamente', justification='center')],
                        [sg.Table(values=data_from_excel, 
                        headings=headings, 
                        max_col_width=35,
                        auto_size_columns=True,
                        display_row_numbers=True,
                        justification='right',
                        num_rows=10,
                        key='-TABLE-',
                        enable_events = True,
                        row_height=35)]
                    ]
    table_window = sg.Window("Información del inventario", table_window_layout)
    while True:
        event, values = table_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    table_window.close()
