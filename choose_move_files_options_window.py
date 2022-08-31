import PySimpleGUI as sg
import choose_destination_window
import pandas as pd

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
    return final_structure


def create(data_from_excel, headings):
    selected_options=[]
    choose_move_file_options_window_layout = [
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
        [sg.Push(), sg.Button("Siguiente", key="-NEXT-", visible=False)]
    ]

    choose_move_file_options_window = sg.Window("Mover archivos", choose_move_file_options_window_layout, size=(400, 500))

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
        
        if event == "Avanzar":
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
            final_structure = create_structure("-", selected_options, data_from_excel)
            choose_move_file_options_window["-TEXT-STRUCTURE-"].update(visible=True)
            choose_move_file_options_window["-EXAMPLE-"].update(final_structure)
            choose_move_file_options_window["-NEXT-"].update(visible=True)

        if event == "_":
            choose_move_file_options_window["-"].update(visible=False)
            choose_move_file_options_window["."].update(visible=False)
            final_structure = create_structure("_", selected_options, data_from_excel)
            choose_move_file_options_window["-TEXT-STRUCTURE-"].update(visible=True)
            choose_move_file_options_window["-EXAMPLE-"].update(final_structure)
            choose_move_file_options_window["-NEXT-"].update(visible=True)

        if event == ".":
            choose_move_file_options_window["_"].update(visible=False)
            choose_move_file_options_window["-"].update(visible=False)
            final_structure = create_structure(".", selected_options, data_from_excel)
            choose_move_file_options_window["-TEXT-STRUCTURE-"].update(visible=True)
            choose_move_file_options_window["-EXAMPLE-"].update(final_structure)
            choose_move_file_options_window["-NEXT-"].update(visible=True)

        if event == "-NEXT-":
            choose_move_file_options_window.close()
            choose_destination_window.create()


 