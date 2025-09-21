import os
import subprocess
import multiprocessing as mp
import pynput
import tkinter as tk
from pynput.keyboard import Key, KeyCode
import read_a_button as rb

def decode(s:bytes):
    if os.uname().sysname == 'linux':
        return s.decode('UTF-8')[:-1]
    else:
        return s.decode('CP1251')[:-1]

def read_button():
    #proc = subprocess.run(["python3", "read_a_button.py"], stdout=subprocess.PIPE)
    #s = proc.stdout
    #print("before_decode= ", s)
    #s = decode(s)
    #print("after_decode= ", s)
    manager = mp.Manager()
    x = manager.list()
    proc = mp.Process(target=rb.main, args=(x,))
    proc.start()
    proc.join()
    proc.terminate()
    #print("x=", x)
    lst = x[0].split()
    #print("after_split= ", lst)
    return lst

def to_KeyCode(x:list):
    ans = KeyCode.from_vk(x[0])
    if len(x[1]) == 1:
        ans.char = x[1]
    else:
        ans.char = None
    return ans

def form(x):
    x = int(str(x)[1:-1])

