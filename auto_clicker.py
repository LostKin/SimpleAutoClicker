import pynput
import pyautogui
import tkinter
import os
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button
import time
import sqlite3
import macrolib as ml

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()
time_to_do_commands = 0
time_between_clicks = 0
delay = 0
ignore = False

s_key = KeyCode.from_vk(0)
stop_key = KeyCode.from_vk(0)


auto_mode = 0
bal = 0

def click():
    global bal, auto_mode, delay, ignore
    while True:
        print("bal=", bal, "auto_mode=", auto_mode)
        sup = time.time()
        if (auto_mode and bal):
            #keyboard.press('a')
            #keyboard.release('a')
            #ignore = True
            mouse.press(Button.left)
            mouse.release(Button.left)
            #ignore = False
        diff = time.time() - sup
        time.sleep(max(0, delay - diff))
        
        
def on_press(key):
    global bal
    #if (key == Key.ctrl_l):
    #    bal += 1
    return
        
def on_release(key):
    global auto_mode, bal
    t = 0
    #print(type(key))
    #print(key==Key.enter, Key.enter._value_ )
    if (type(key) == Key):
        t = int(str(key._value_)[1:-1])
        #os.system("nemo")
    else:
        t = key.vk
    if (t == s_key.vk):
        """for i in range(10):
            mouse.press(Button.left)
            mouse.release(Button.left)
            time.sleep(0.1)"""
        
        auto_mode = 1 - auto_mode
        if (not(auto_mode)):
            print("OFF")
            bal = 0
        else:
            print("ON")
        #print("in_on = ", auto_mode, "  mouse_press_balance =",  bal)
    #if (key == Key.ctrl_l):
    #    bal -= 1

        
def on_click(mouse_x, mouse_y, button, pressed):
    global bal
    if (ignore):
        return
    if (button == Button.left):
        if (pressed):
            #print("LOL")
            bal += 1
        else:
            bal -= 1
            
        
#fin = open("config.txt", "r")
#time_between_clicks = int(fin.readline().split('=')[1])
#time_to_do_commands = int(fin.readline().split('=')[1])
#delay = max(time_between_clicks - time_to_do_commands, 0) / 1000

keyboard_listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = pynput.mouse.Listener(on_click=on_click)
db = sqlite3.connect(".\config.db") 
master = 0

def start():
    global master
    #master = tkinter.Tk()
    #is_on = tkinter.Label(text="MACROS PAUSED", fg='black')
    global s_key, delay, stop_key
    db = sqlite3.connect(".\config.db") 
    cursor = db.cursor()
    cursor.execute('''SELECT id FROM conf WHERE name = ?''', ("pause",))
    x = cursor.fetchone()[0]
    s_key = KeyCode.from_vk(x)
    """cursor.execute('''SELECT id FROM conf WHERE name = ?''', ("stop",))
    x = cursor.fetchone()[0]
    stop_key = KeyCode.from_vk(x)"""    
    cursor.execute('''SELECT cnt FROM nums WHERE name = ?''', ("cps",))
    x = cursor.fetchone()[0]    
    delay = 1 / max(x, 1)
    #delay = delay / 1000
    keyboard_listener.start()
    mouse_listener.start()
    click()
    master.mainloop()
    keyboard_listener.join()
    mouse_listener.join()
    
def stop():
    global master
    db.close()
    keyboard_listener.stop()
    mouse_listener.stop()
    master.destroy()

