from flask import Flask, render_template, request
import ctypes
from ctypes import wintypes
import time

app = Flask(__name__)

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyboardInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyboardInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

def press_key(scancode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyboardInput(0, scancode, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release_key(scancode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyboardInput(0, scancode, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

SCANCODES = {
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
}

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        button_name = request.form.get('button')
        if button_name:
            print(f"Получено значение кнопки: {button_name}")
            if button_name == 'Motion 3':
                print("Нажатие клавиши '3' для режима 'Ход 3'")
                press_key(SCANCODES['3'])
                time.sleep(0.05)
                release_key(SCANCODES['3'])
            elif button_name == 'Braking 3':
                print("Нажатие клавиши '7' для режима 'Торможение 3'")
                press_key(SCANCODES['7'])
                time.sleep(0.05)
                release_key(SCANCODES['7'])
            elif button_name == 'Motion 2':
                print("Нажатие клавиши '2' для режима 'Ход 2'")
                press_key(SCANCODES['2'])
                time.sleep(0.05)
                release_key(SCANCODES['2'])
            elif button_name == 'Braking 2':
                print("Нажатие клавиши '6' для режима 'Торможение 2'")
                press_key(SCANCODES['6'])
                time.sleep(0.05)
                release_key(SCANCODES['6'])
            elif button_name == 'Motion 1':
                print("Нажатие клавиши '1' для режима 'Ход 1'")
                press_key(SCANCODES['1'])
                time.sleep(0.05)
                release_key(SCANCODES['1'])
            elif button_name == 'Braking 1':
                print("Нажатие клавиши '5' для режима 'Торможение 1'")
                press_key(SCANCODES['5'])
                time.sleep(0.05)
                release_key(SCANCODES['5'])
            elif button_name == 'Coasting':
                print("Нажатие клавиши '4' для режима 'Выбег'")
                press_key(SCANCODES['4'])
                time.sleep(0.05)
                release_key(SCANCODES['4'])
        else:
            print("Значение кнопки не получено")
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)