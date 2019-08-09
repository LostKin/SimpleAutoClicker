import os
import subprocess
import pynput
import tkinter as tk
from pynput.keyboard import Key, KeyCode

def decode(s:bytes):
    if os.uname().sysname == 'linux':
        return s.decode('UTF-8')[:-1]
    else:
        return s.decode('CP1251')[:-1]

def read_button():
    proc = subprocess.run(["python3", "read_a_button.py"], stdout=subprocess.PIPE)
    s = proc.stdout
    #print("before_decode= ", s)
    s = decode(s)
    #print("after_decode= ", s)
    lst = s.split()
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

