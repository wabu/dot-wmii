from wmiirc import *

import threading
import os
import re

space = re.compile('\s+')
info = []

cmd="top -d4 -b -o '+%CPU' | sed -un '6p; /^  PID/{N;s/.*\\n//;p}'"
col=['pid', 'user', 'pr', 'ni', 'virt', 'res', 'shr', 's', 'cpu', 'mem', 'time', 'cmd']

@defmonitor(name='42-top', interval=20)
def top(self):
    dct = dict(zip(col, info))
    return wmii.cache['normcolors'], dct['cpu'] + ' ' + dct['cmd']

def top_listen():
    global info
    reset = True
    with os.popen(cmd) as p:
        while True:
            line = p.readline()
            if not line:
                break
            parts = space.split(line.strip())
            if not parts:
                continue
            info = parts
            top.tick()

if 'top_reader' not in vars():
    top_reader = threading.Thread(target=top_listen)
    top_reader.start()
