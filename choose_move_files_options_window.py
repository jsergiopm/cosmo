import PySimpleGUI as sg
import pandas as pd
import move_files_progress_window
import cosmo


def create_structure(separator, selected_options, data_from_excel):
    indexes = []
    final_structure = ""
    size_selection = len(selected_options)
    for i in range(size_selection):
        indexes.append(data_from_excel[0].index(selected_options[i]))
        tmp = data_from_excel[1][indexes[i]]
        if pd.isna(tmp):
            pass
        else:
            final_structure = "%s%s" % (final_structure, data_from_excel[1][indexes[i]])
            if i + 1 == size_selection:
                break
            else:
                final_structure = final_structure + separator
    filenames = []
    for row in range(len(data_from_excel)):
        filename = ""
        if row > 0:
            for i in range(len(indexes)):
                if pd.isna(filename):
                    pass
                else:
                    filename = "%s%s" %(filename, data_from_excel[row][indexes[i]])
                    if i + 1 == len(indexes):
                        break
                    else:
                        filename += separator
            filenames.append(filename)
        
    return final_structure, filenames


def create(data_from_excel, headings, source_path, destination_path, subfolder):
    selected_options=[]
    choose_move_file_options_window_layout = [
        [sg.Button("Volver al inicio"), sg.Push()],
        [sg.Text('Selecciona el nombre que tendrán las carpetas: ')],
        [sg.Listbox(headings, disabled=False, size=(20, len(headings)), key='-HEADINGS-', visible=True),
        sg.Push(),
        sg.Listbox(selected_options, size=(20, len(headings)), key='-SELECTION-', disabled=False)],
        [sg.Text(size=(25,1), key='-STRUCTURE-')],
        [sg.Button("Agregar", button_color=('white', 'green')),
        sg.Button("Quitar", button_color=('white', 'red')),
        sg.Push(), sg.Button("Avanzar", disabled=False)],
        [sg.Text('Selecciona el separador: ', key='-SEPARATOR-', visible = False)],
        [sg.Button('-', visible=False), sg.Button('_', visible=False), sg.Button('.', visible=False),],
        [sg.Text("La estructura de las carpetas quedará así: ", key ="-TEXT-STRUCTURE-", visible=False)],
        [sg.Text(size=(100,1), key="-EXAMPLE-")],
        [sg.Text('Selecciona la columna del inventario que hace referencia al nombre del archivo', key='-SELECTED COLUMN-', visible=False)],
        [sg.Combo(headings, default_value="N° Identificación", key='-Combo-', visible=False), sg.Push(), sg.Button("Mover archivos", key="-NEXT-", visible=False) ],
        []
    ]

    choose_move_file_options_window = sg.Window("Mover archivos", choose_move_file_options_window_layout, icon="./assets/favicon.ico", size=(500, 600))

    while True:
        event, values = choose_move_file_options_window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Agregar":
            try:
                selected_options.append(values['-HEADINGS-'][0])
                choose_move_file_options_window['-SELECTION-'].update(selected_options)
            except:
                sg.popup("Debe seleccionar una opción del listado")        
        if event == "Quitar":
            try:
                selected_options.remove(values['-SELECTION-'][0])
            except:
                pass    
            choose_move_file_options_window['-SELECTION-'].update(selected_options)
        
        if event == "Avanzar" and len(selected_options) > 0:
            choose_move_file_options_window["-HEADINGS-"].update(disabled=True)
            choose_move_file_options_window["-SELECTION-"].update(disabled=True)
            choose_move_file_options_window["-SEPARATOR-"].update(visible=True)
            choose_move_file_options_window["-"].update(visible=True)
            choose_move_file_options_window["_"].update(visible=True)
            choose_move_file_options_window["."].update(visible=True)
            choose_move_file_options_window["Avanzar"].update(disabled=True)
        
        if event == "-":
            choose_move_file_options_window["_"].update(visible=False)
            choose_move_file_options_window["."].update(visible=False)
            choosed_sepatator = "-"
            final_structure, filenames = create_structure(choosed_sepatator, selected_options, data_from_excel)
            choose_move_file_options_window["-TEXT-STRUCTURE-"].update(visible=True)
            choose_move_file_options_window["-EXAMPLE-"].update(final_structure)
            choose_move_file_options_window["-SELECTED COLUMN-"].update(visible=True)
            choose_move_file_options_window["-Combo-"].update(visible=True)
            choose_move_file_options_window["-NEXT-"].update(visible=True)

        if event == "_":
            choose_move_file_options_window["-"].update(visible=False)
            choose_move_file_options_window["."].update(visible=False)
            choosed_sepatator = "_"
            final_structure, filenames = create_structure(choosed_sepatator, selected_options, data_from_excel)
            choose_move_file_options_window["-TEXT-STRUCTURE-"].update(visible=True)
            choose_move_file_options_window["-EXAMPLE-"].update(final_structure)
            choose_move_file_options_window["-SELECTED COLUMN-"].update(visible=True)
            choose_move_file_options_window["-Combo-"].update(visible=True)
            choose_move_file_options_window["-NEXT-"].update(visible=True)

        if event == ".":
            choose_move_file_options_window["_"].update(visible=False)
            choose_move_file_options_window["-"].update(visible=False)
            choosed_sepatator = "."
            final_structure, filenames = create_structure(choosed_sepatator, selected_options, data_from_excel)
            choose_move_file_options_window["-TEXT-STRUCTURE-"].update(visible=True)
            choose_move_file_options_window["-EXAMPLE-"].update(final_structure)
            choose_move_file_options_window["-SELECTED COLUMN-"].update(visible=True)
            choose_move_file_options_window["-Combo-"].update(visible=True)
            choose_move_file_options_window["-NEXT-"].update(visible=True)


        if event == "-NEXT-":
            column = headings.index(values["-Combo-"])
            choose_move_file_options_window.close()
            move_files_progress_window.create(source_path, destination_path, subfolder, filenames, data_from_excel, column)
        
        if event == 'Volver al inicio':
            choose_move_file_options_window.close()
            cosmo.run()
 