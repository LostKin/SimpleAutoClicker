import tkinter as tk
import pynput
from pynput.keyboard import Key, KeyCode
import os
from tkinter import Button
#import subprocess
import macrolib as ml
import auto_clicker as ac
import sqlite3
import multiprocessing as mp

# взять текст tk.Label().cget("text")    

class FloatingWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.overrideredirect(True)

        #self.label = tk.Label(self, text="Click on the grip to move")
        #self.grip = tk.Label(self, bitmap="gray25")
        #self.grip.pack(side="left", fill="y")
        #self.label.pack(side="right", fill="both", expand=True)

        self.bind("<ButtonPress-1>", self.StartMove)
        self.bind("<ButtonRelease-1>", self.StopMove)
        self.bind("<B1-Motion>", self.OnMotion)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))



db = sqlite3.connect("./config.db")
cursor = db.cursor()


def edit(lbl:tk.Label, text:str):
    lbl.config(text=text)
    lbl.update()

def read_numeric_str(label:tk.Button):
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
    cps.config(text=d)
    cps.update()
    num = 0
    read_numeric_str(cps)
    s = cps.cget("text")[len(d):]
    s = int(s)
    s = min(s, 1000)
    cursor.execute("UPDATE nums SET cnt = ? WHERE name = ?", (s, "cps"))
    db.commit()
    
def SetPauseButton():
    d = 'MACROS PAUSE BUTTON : '
    spause.config(text=d)
    spause.update()
    x = ml.read_button()
    cursor.execute("UPDATE conf SET id = ? WHERE name = ?", (x[0], "pause"))
    cursor.execute("UPDATE conf SET cur_name = ? WHERE name = ?", (x[1], "pause"))
    db.commit()
    spause.config(text=d + x[1])
    spause.update()    

proc = 0;

def start_m():
    global com
    com.pop()
    com.append(0)
    global proc
    #print("KEK")
    start.config(text="STOP MACROS", command=stop_m)
    start.update()
    #print("LOL")
    proc = mp.Process(target=ac.start, args=(com,))
    proc.start()
    #proc.join()
    
def stop_m():
    global proc
    start.config(text="START MACROS", command=start_m)
    start.update()    
    #print("KEK")    
    proc.terminate()
    #proc.communicate("")


def exit():
    global proc
    if type(proc) != int:
        stop_m()
    master.destroy()


def upd():
    global com
    if com[0]:
        #is_paused.config(text='MACROS UNPAUSED')
        is_paused.config(background='green')
        #print("on")
    else:
        is_paused.config(background='red')
        #is_paused.config(text='MACROS PAUSED')
        #print("off")
    is_paused.update()
    #sub_master.lift()
    master.after(1000, upd)

if __name__ == "__main__":
    mp.freeze_support()
    man = mp.Manager()
    com = man.list()
    com.append(0)
    master = tk.Tk(className=' SimpleAutoClicker')
    sub_master = FloatingWindow(master)
    #sub_master = tk.Toplevel(master)
    #sub_master.geometry('100x100')
    #canvas = tk.Canvas(master, width=800, height=600, background='white')
    #canvas.pack()

    frame = tk.Frame(master)
    frame.pack()

    cursor.execute('''SELECT cur_name FROM conf WHERE name = ?''', ("pause",))
    c_pause = cursor.fetchone()[0]
    pause = tk.Button(frame, background='white', fg='black', text='SET PAUSE BUTTON')
    pause.grid(row=0, column=0, ipadx=30, padx=10)
    #pause.pack(fill=tk.X)

    cursor.execute('''SELECT cnt FROM nums WHERE name = ?''', ("cps",))
    c_cps = cursor.fetchone()[0]
    clicks = tk.Button(frame, background='white', fg='black', text='SET CLICKS PER SEC')
    clicks.grid(row=1, column=0, ipadx=30, padx=10)
    #clicks.pack(fill=tk.X)

    quit = tk.Button(frame, text=' ' * 8 + 'QUIT' + ' ' * 8, fg='red', command=exit, background='white')
    quit.grid(row=5, column=0, ipadx=10)
    #quit.pack(padx=5, pady=20, side=tk.LEFT)

    start = tk.Button(frame, text='START MACROS', fg='black', background='white', command=start_m)
    start.grid(row=5, column=1, ipadx=10)
    #start.pack(padx=5, pady=20, side=tk.LEFT)

    #stop = tk.Button(frame, text='STOP MACROS', fg='black', background='white', command=stop)
    #stop.grid(row=5, column=2, ipadx=10, padx=10)
    #stop.pack(padx=5, pady=20, side=tk.LEFT)

    cps = tk.Entry(frame, fg='black', background='white')
    cps.grid(row=1, column=1, ipadx=30, padx=10)

    spause = tk.Button(frame, text='MACROS PAUSE BUTTON : ' + c_pause, fg='black', background='white', command=SetPauseButton)
    spause.grid(row=0, column=1, ipadx=30, padx=10)

    #is_paused = tk.Label(sub_master, text="MACROS PAUSED", fg='black', background='white')
    #is_paused.grid(row=3, column=3)
    is_paused = tk.Canvas(sub_master, background='red', height=40, width=40)
    is_paused.pack()
    #stop = tk.Label(frame, text='MACROS STOP BUTTON : ')
    master.after(1000, upd)
    #master.call('wm', 'attributes', '.', '-topmost', '1')
    #x = list(master.wm_attributes())
    #x[3] = 1
    #print(master.__dict__)
    #print(master)
    #print(sub_master.wm_attributes())
    sub_master.attributes('-topmost', True)
    #sub_master.attributes('-disabled', True)
    #sub_master.overrideredirect(1)
    #sub_master.configure(background="black")
    sub_master.update()
    master.mainloop()
    sub_master.mainloop()
    db.close()