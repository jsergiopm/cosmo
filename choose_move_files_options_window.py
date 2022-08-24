from pydoc import visiblename
import PySimpleGUI as sg
 
def create(data_from_excel, headings):
    selected_options=[]
    choose_move_file_options_window_layout = [
        [sg.Text('Selecciona el nombre que tendrán las carpetas: ')],
        [sg.Listbox(
          headings,
          disabled=False,
          size=(15, len(headings)),
          key='-HEADINGS-',
          visible=True,
          ),
        sg.Listbox(selected_options, size=(15, len(headings)), key='-SELECTION-', disabled=False)],
        [sg.Text(size=(25,1), key='-STRUCTURE-')],
        [sg.Button("Agregar", button_color=('white', 'green')),
        sg.Button("Quitar", button_color=('white', 'red')),
        sg.Button("Siguiente")],
        [sg.Text('Selecciona el separador: ', key='-SEPARATOR-', visible = False)],
        [sg.Button('-', visible=False), sg.Button('_', visible=False), sg.Button('.', visible=False),]
    ]

    choose_move_file_options_window = sg.Window("Mover archivos", choose_move_file_options_window_layout)

    while True:
        event, values = choose_move_file_options_window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Agregar":
            selected_options.append(values['-HEADINGS-'][0])
            choose_move_file_options_window['-SELECTION-'].update(selected_options)
        
        if event == "Quitar":
            try:
                selected_options.remove(values['-SELECTION-'][0])
            except:
                pass    
            choose_move_file_options_window['-SELECTION-'].update(selected_options)
        
        if event == "Siguiente":
            choose_move_file_options_window["-HEADINGS-"].update(disabled=True)
            choose_move_file_options_window["-SELECTION-"].update(disabled=True)
            choose_move_file_options_window["-SEPARATOR-"].update(visible=True)
            choose_move_file_options_window["-"].update(visible=True)
            choose_move_file_options_window["_"].update(visible=True)
            choose_move_file_options_window["."].update(visible=True)

 