import PySimpleGUI as sg
import change_filename_window
import move_files_window


def run():
    #file_name, folder_name, status = read_csv()
    #move_file(file_name, folder_name, status)
    sg.theme("LightBrown3")

    main_window_layout = [
        [
            sg.T("")
        ],
        [sg.Text('Bienvenido a Cosmo', size=(30, 1), justification='center', font=("Helvetica", 25))],
        [sg.Text('Selecciona la instrucción que vas a ejecutar')], 
        [
        sg.Button("Cambiar"),
        sg.Button("Mover archivos"),
        ],  
    ]

    main_window = sg.Window('Cosmo', main_window_layout, size=(330,150))

    while True:
        event, values = main_window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            break
        elif event == "Cambiar":
            main_window.Close()
            change_filename_window.create()

        elif event == "Mover archivos":
            main_window.close()
            move_files_window.create()
            


if __name__ == "__main__":
    run()