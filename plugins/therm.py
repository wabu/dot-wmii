# -*- coding: utf-8 -*- 

from wmiirc import *
import os

colors = [(90, 'errorcolors'),
          (70, 'noticecolors'),
          (50, 'focuscolors'),
          (0, 'normcolors')]

schemata = (('normal', None, [(90, 1800),
                              (80, 2600),
                              (70, 3600)]),
            ('quiet', 'successcolors', [(70, 1600),
                                        (65, 2000),
                                        (50, 2600)]),
            ('minimal', 'noticecolors', [(40, 800), 
                                         (30, 1200)]))
zones = [0, 1]
inputs = ['/sys/devices/virtual/thermal/thermal_zone%d/temp' % z for z in zones]

def read(input):
    with open(input) as f:
        return int(f.read())/1000

def info():
    with os.popen('acpitool -cf') as f:
        nfo = f.read().split()
    return nfo[25], nfo[6]

last = 0
mode = 'normal'

@defmonitor(interval=4, name='46-thermal')
def thermal(self):
    global last
    global mode

    temp = max(map(read, inputs))

    for t, color in colors:
        if temp >= t:
            break

    co, ts = {m: (co, ts) for m, co, ts in schemata}[mode]
    for t, freq in ts:
        if temp >= t:
            break

    if last != freq:
        print('sitting cpu limit to %d, as core is %d' % (freq, temp))
        os.system('sudo cpupower frequency-set -u %dMhz > /dev/null' % freq)
        last = freq
    
    line = wmii.cache[co or color][2]

    freq, rpm = info()

    return (wmii.cache[color][:2] + [line],
            u'{}° @{:0.1f}GHz %{}'.format(temp, float(freq)/1000, rpm))


def toggle_thermal():
    global mode

    lst = [m for m, _, __ in schemata]
    i = lst.index(mode) + 1
    mode = lst[i % len(lst)]

    thermal.tick()

wmii.toggle_thermal = toggle_thermal
