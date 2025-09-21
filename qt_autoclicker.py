import pynput

from PyQt5.QtCore import QObject, pyqtSignal
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button
import time
import ctypes

class AutoClicker(QObject):
    update_state = pyqtSignal(bool)

    def __init__(self, cps, pause_key):

        super().__init__()
        self.delay = None
        self.stop = True
        self.keyboard = pynput.keyboard.Controller()
        self.mouse = pynput.mouse.Controller()

        self.cps = cps
        self.pause_key = pause_key
        self.delay = 1 / self.cps

        self.ignore = False

        self.is_active = False
        self.balance = 0

        self.keyboard_listener = pynput.keyboard.Listener(on_release=self.on_release)
        self.mouse_listener = pynput.mouse.Listener(on_click=self.on_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def set_cps(self, cps):
        self.cps = cps
        self.delay = 1 / self.cps

    def set_pause_key(self, pause_key):
        self.pause_key = pause_key

    def on_release(self, key):
        t = 0
        if self.stop:
            return
        try:
            print(type(key))
            t = None
            if type(key) == Key:
                t = key.name
                # os.system("nemo")
            elif type(key) == KeyCode:
                t = key.char
            if t == self.pause_key.lower() or t == self.pause_key.upper() or t == self.pause_key:
                """for i in range(10):
                    mouse.press(Button.left)
                    mouse.release(Button.left)
                    time.sleep(0.1)"""

                self.is_active = not self.is_active
                if not self.is_active:
                    print("OFF")
                    self.balance = 0
                    self.update_state.emit(False)
                else:
                    print("ON")
                    self.update_state.emit(True)
        except:
            return

    def on_click(self, mouse_x, mouse_y, button, pressed):
        if self.ignore:
            return
        if button == Button.left:
            if pressed:
                # print("LOL")
                self.balance += 1
            else:
                self.balance -= 1

    def update_mainloop(self, signal):
        self.stop = signal

    def die(self):
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def emulate_click(self):

        PUL = ctypes.POINTER(ctypes.c_ulong)

        class MouseInput(ctypes.Structure):
            _fields_ = [("dx", ctypes.c_long),
                        ("dy", ctypes.c_long),
                        ("mouseData", ctypes.c_ulong),
                        ("dwFlags", ctypes.c_ulong),
                        ("time", ctypes.c_ulong),
                        ("dwExtraInfo", PUL)]

        class Input(ctypes.Structure):
            _fields_ = [("type", ctypes.c_ulong),
                        ("mi", MouseInput)]

        SendInput = ctypes.windll.user32.SendInput
        # Mouse down
        mi = MouseInput(0, 0, 0, 0x0002, 0, None)
        inp = Input(0, mi)
        SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

        #
        time.sleep(0.02)

        # Mouse up
        mi = MouseInput(0, 0, 0, 0x0004, 0, None)
        inp = Input(0, mi)
        SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

    def mainloop(self):
        print("mainloop started")
        while True:
            # print("bal=", bal, "auto_mode=", auto_mode)
            if self.stop:
                break
            sup = time.time()
            if self.is_active and self.balance:
                #self.mouse.press(Button.left)
                #self.mouse.release(Button.left)
                #mouse.click("left")
                self.emulate_click()
            diff = time.time() - sup
            time.sleep(max(0, self.delay - diff))
        print("mainloop stopped")

