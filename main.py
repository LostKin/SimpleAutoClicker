import tkinter as tk
import pynput
from pynput.keyboard import Key, KeyCode
import os
from tkinter import Button
import subprocess
import macrolib as ml
import auto_clicker as ac
import sqlite3
import multiprocessing as mp
    
# взять текст tk.Label().cget("text")    

db = sqlite3.connect("./config.db")
cursor = db.cursor()

def edit(lbl:tk.Label, text:str):
    lbl.config(text=text)
    lbl.update()

def read_numeric_str(label:tk.Label):
    now = ''
    while now != Key.enter._value_:
        #print(now, Key.enter)
        x = ml.read_button()
        #print("raw_key= ", x)
        if (x[0] != ''):
            x[0] = int(x[0])
            now = ml.to_KeyCode(x)
            if now.vk == Key.enter._value_:
                return
            print(now.vk, Key.backspace._value_)
            if now.vk == int(str(Key.backspace._value_)[1:-1]):
                text = label.cget("text")
                if text[-1] != ' ':
                    text = text[:-1]
                    edit(label, text)
            if now.char and len(now.char) == 1 and now.char in "1234567890":
                #print("LUL")
                text = (label.cget("text") + now.char)
                #print(text)
                edit(label, text)
                #cur_str.config(text=text)


def SetClicksPerSec():
    d = 'CLICKS PER SEC : '
    clicks.config(text=d)
    clicks.update()
    num = 0
    read_numeric_str(clicks)
    s = clicks.cget("text")[len(d):]
    s = int(s)
    s = min(s, 1000)
    cursor.execute("UPDATE nums SET cnt = ? WHERE name = ?", (s, "cps"))
    db.commit()
    
def SetPauseButton():
    d = 'MACROS PAUSE BUTTON : '
    pause.config(text=d)
    pause.update()
    x = ml.read_button()
    cursor.execute("UPDATE conf SET id = ? WHERE name = ?", (x[0], "pause"))
    cursor.execute("UPDATE conf SET cur_name = ? WHERE name = ?", (x[1], "pause"))
    db.commit()
    pause.config(text=d + x[1])
    pause.update()    

proc = 0;

def start():
    global proc
    proc = mp.Process(target=ac.start)
    proc.start()
    #proc.join()
    
def stop():
    global proc
    proc.terminate()
    #proc.communicate("")

master = tk.Tk(className=' SimpleAutoClicker')
#canvas = tk.Canvas(master, width=800, height=600, background='white')
#canvas.pack()

frame = tk.Frame(master)
frame.pack()

cursor.execute('''SELECT cur_name FROM conf WHERE name = ?''', ("pause",))
c_pause = cursor.fetchone()[0]
pause = tk.Label(frame, background='white', fg='black', text='MACROS PAUSE BUTTON : ' + c_pause)
pause.grid(row=0, column=1, ipadx=30, padx=10)
#pause.pack(fill=tk.X)

cursor.execute('''SELECT cnt FROM nums WHERE name = ?''', ("cps",))
c_cps = cursor.fetchone()[0]
clicks = tk.Label(frame, background='white', fg='black', text='CLICKS PER SEC : ' + str(c_cps))
clicks.grid(row=1, column=1, ipadx=30, padx=10)
#clicks.pack(fill=tk.X)

quit = tk.Button(frame, text=' ' * 8 + 'QUIT' + ' ' * 8, fg='red', command=quit, background='white')
quit.grid(row=5, column=0, ipadx=10)
#quit.pack(padx=5, pady=20, side=tk.LEFT)

start = tk.Button(frame, text='START MACROS', fg='black', background='white', command=start)
start.grid(row=5, column=1, ipadx=10)
#start.pack(padx=5, pady=20, side=tk.LEFT)

stop = tk.Button(frame, text='STOP MACROS', fg='black', background='white', command=stop)
stop.grid(row=5, column=2, ipadx=10, padx=10)
#stop.pack(padx=5, pady=20, side=tk.LEFT)

cps = tk.Button(frame, text='SET CLICKS PER SEC', fg='black', background='white', command=SetClicksPerSec)
cps.grid(row=1, column=0, ipadx=30, padx=10)

spause = tk.Button(frame, text='SET PAUSE BUTTON', fg='black', background='white', command=SetPauseButton)
spause.grid(row=0, column=0, ipadx=30, padx=10)

#stop = tk.Label(frame, text='MACROS STOP BUTTON : ')

master.mainloop()
db.close()