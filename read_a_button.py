import pynput
from pynput.keyboard import Key
from pynput.keyboard import KeyCode
from pynput.mouse import Button
import time

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()

def on_press(key):
    return

def on_release(key):
    if (type(key) != Key and key != Key.shift and key != Key.shift_r):
        print(str(key.vk) + ' ' + key.char)
    else:
        print(str(key._value_)[1:-1] + ' ' + key._name_)
    #print(type(key) == KeyCode)
    keyboard_listener.stop()
    return

keyboard_listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()
keyboard_listener.join()