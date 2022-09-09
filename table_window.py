import PySimpleGUI as sg
import choose_move_files_options_window

def create(data_from_excel, headings):
    data_to_show =[]
    for i in range(12):
        if i > 1:
            data_to_show.append(data_from_excel[i])

    table_window_layout = [
                        [sg.Text('Vista previa del inventario: ', justification='center')],
                        [sg.Table(values=data_to_show, 
                        headings=headings, 
                        max_col_width=35,
                        auto_size_columns=True,
                        justification='right',
                        vertical_scroll_only = False,
                        num_rows=10,
                        key='-TABLE-',
                        row_height=35)],
                        [sg.Text('Solo se muestran los 10 primeros registros')],
                        [sg.Push(), sg.Button('Siguiente')]
                    ]
    table_window = sg.Window("Información del inventario", table_window_layout, element_justification='c', size=(1000, 500))
    while True:
        event, values = table_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Siguiente":
            table_window.close()
            choose_move_files_options_window.create(data_from_excel, headings)

            
