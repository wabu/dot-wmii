from wmiirc import *
import os
import threading

base = '/sys/class/power_supply/BAT0/'
def bs_read(what):
    try:
        with open(base + what) as f:
            return f.read().strip()
    except IOError:
        return ''

last = -100
est = -1
stat = ''

@defmonitor(name='92-battery', interval=6)
def battery(self):
    global last, est, stat

    status = bs_read('status') or 'unknown'
    perc = (float(bs_read('charge_now') or
                  bs_read('energy_now') or 0) /
            float(bs_read('charge_full') or
                  bs_read('energy_full') or 1) * 100)

    color = 'normcolors'
    fmt = '=[%2.0f%%/%s]'
    if status == 'Discharging':
        fmt = 'v[%2.0f%%/%s]'
        if perc < 15:
            color = 'errorcolors'
        elif perc < 50:
            color = 'noticecolors'
        elif perc < 70:
            color = 'successcolors'
    elif status == 'Charging':
        fmt = '^[%2.0f%%/%s]'
        if perc < 50:
            color = 'focuscolors'
    elif status == 'unknown':
        fmt = '?[%2.0f%%/%s]'
        perc = perc or last
        color = 'noticecolors'

    if abs(perc - last) > 2 or status != stat:
        last = perc
        stat = status
        with os.popen('acpitool') as p:
            info = p.read().split()
        if len(info) > 5 and ':' in info[5]:
            h,m,s = map(int, info[5].split(':'))
            est = h * 60 + m - m % 5
        else:
            est = '???' if status == 'unknown' else '-'

    return wmii.cache[color], fmt % (perc, est)

def acpi_listen():
    with os.popen('acpi_listen') as p:
        while True:
            line = p.readline()
            if not line:
                break
            battery.tick()


if 'acpi_reader' not in vars():
    acpi_reader = threading.Thread(target=acpi_listen)
    acpi_reader.start()
