import eel
from HAND_asl import asl_mode
from HAND_rc import remotecontrol_mode
from HAND_mouse import mouse_mode
from HAND_keyboard import keyboard_mode
from HAND_game import game_mode

public_path = 'public'
eel.init(public_path)

@eel.expose
def call_mouse_mode():
    mouse_mode()

@eel.expose
def call_keyboard_mode():
    keyboard_mode()

@eel.expose
def call_asl_mode():
    asl_mode()

@eel.expose
def call_rc_mode():
    remotecontrol_mode()

@eel.expose
def call_game_mode():
    game_mode()

# -function to run when app is closed
def close_callback(route, websockets):
    if not websockets:
        print('Good Bye!')
        exit()

# -parameters
mode = 'chrome'
size = (612, 438)
position = (100, 100)
port = 8000
disable_cache = True
cmdline_args = ['--incognito']

# -start the app
eel.start('index.html', mode=mode, size=size, position=position, port=port,
          disable_cache=disable_cache, close_callback=close_callback, cmdline_args=cmdline_args)