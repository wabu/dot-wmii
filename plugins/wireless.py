from wmiirc import *
import threading
import os
import re
import time
import wpactrl

interface = 'wlp3s0'
socket = '/var/run/wpa_supplicant/' + interface

if 'wpa' not in vars():
    wpa = wpactrl.WPACtrl(socket)
    wpa_event = wpactrl.WPACtrl(socket)


nil = re.match('()', '')
def wpa_get(info, key):
    return (re.search('\n%s=(.*)\n' % key, info) or nil).group(1)


@defmonitor(name='87-wireless', interval=6)
def wireless(self):
    info = wpa.request('STATUS')
    state = wpa_get(info, 'wpa_state')
    ssid = wpa_get(info, 'ssid')
    mode = wpa_get(info, 'mode')
    ip = wpa_get(info, 'ip_address')
    fmt = '??%s??'
    colors = 'noticecolors'
    if state == 'COMPLETED':
        if mode == 'station':
            fmt = '(%s)'
        else:
            fmt = '<%s>'
        if ip:
            fmt = fmt % fmt
            colors = 'normcolors'
        else:
            fmt = fmt % '>%s<'
    elif ssid:
        fmt = '(~%s~)'
    elif state == 'INTERFACE_DISABLED':
        colors = 'focuscolors'
        fmt = '(~%s~)'
        state = '_'
    return wmii.cache[colors], fmt % (ssid or state.lower())


def wpa_listen():
    wpa_event.attach()
    while wpa_event.attached:
        wpa_event.recv()
        wireless.tick()
        
if 'wpa_reader' not in vars():
    wpa_reader = threading.Thread(target=wpa_listen)
    wpa_reader.start()
