import PySimpleGUI as sg
import change_filename_window
import move_files_window
import take_out_files_window


def play_intro():
    FILENAME = r'../assets/intro_img.png'
    DISPLAY_TIME_MILLISECONDS = 4000

    sg.Window('Window Title', [[sg.Image(FILENAME)]], size=(500,500), transparent_color=sg.theme_background_color(), no_titlebar=True, keep_on_top=True).read(timeout=DISPLAY_TIME_MILLISECONDS, close=True)


def run():

    sg.theme('LightGrey1')
    main_window_layout = [
        [
            sg.T("")
        ],
        [sg.Text('Bienvenido a Cosmo', size=(30, 1), justification='center', font=("Helvetica", 25))],
        [sg.Push(), sg.Text('Selecciona la instrucción que vas a ejecutar'), sg.Push()], 
        [
        sg.Button("Cambiar nombre"),
        sg.Button("Mover archivos"),
        sg.Button("Sacar archivos")
        ],
    ]

    main_window = sg.Window('Cosmo',main_window_layout, icon="../assets/favicon.ico", size=(340,150))

    while True:
        event, values = main_window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            break
        elif event == "Cambiar nombre":
            main_window.close()
            change_filename_window.create()

        elif event == "Mover archivos":
            main_window.close()
            move_files_window.create()

        elif event == "Sacar archivos":
            main_window.close()
            take_out_files_window.create()
            

if __name__ == "__main__":
    play_intro()
    run()