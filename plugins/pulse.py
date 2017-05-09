from wmiirc import *
import re
import os
import threading


def pa_parse_inner(data, depth=1):
    data = data.strip()
    if '\n' + '\t'*depth not in data:
        return re.sub('\n\t*', ' ', data)
    items = {}
    for item in re.split('\n' + '\t'*depth + '(?=\w)', data):
        item, data = re.split(':| = ', item, 1)
        items[item.strip(': \t\n')] = pa_parse_inner(data, depth+1)
    return items


def pa_parse(out, depth=0):
    out = out.strip()
    if ':' not in out:
        return out
    items = {}
    for item in re.split('\n(?=\w)', out):
        item, data = item.split('\n', 1)
        items[item] = pa_parse_inner(data)
    return items


def pactl(cmd, bg=True):
    return call('pactl', '--', *cmd.split(' '), background=bg)


@defmonitor(interval=0, name='80-volume')
def volume(self):
    info = pa_parse(pactl('list sinks', bg=False))
    master = next(iter(info.values()))
    vol = int(re.sub('.* (\d+)%.*', r'\1', master['Volume']))
    mute = master['Mute'] == 'yes'
    state = master['State']
    if state == 'RUNNING':
        colors = 'noticecolors' if mute else 'successcolors'
    else:
        colors = 'focuscolors' if mute else 'normcolors'
    out = '=-.' if 'headphone' in master['Active Port'] else '<))'
    return wmii.cache[colors], u'%s%3d%%' % (out, vol)


def pa_listen():
    print('open pactl ...')
    with os.popen('pactl subscribe') as p:
        while True:
            line = p.readline()
            if not line:
                break
            if 'sink' in line:
                volume.tick()

def pa_switcher():
    with os.popen('pactl list sinks') as p:
        out = p.read()
        _, sel = out.split('Ports:\n')
        sel, act = sel.split('Active Port:')
        ports = [l.split(':')[0].strip() 
                for l in sel.split('\n') if l.startswith('\t\t')]
        active = act.split('\n')[0].strip()
    
    new = ports[(ports.index(active) + 1) % len(ports)]
    pactl('set-sink-port 0 %s' % new)


if 'pa_reader' not in vars():
    pa_reader = threading.Thread(target=pa_listen)
    pa_reader.start()


events.bind({
    Match('RightBarMouseDown', 1, volume.name):
        lambda *a: call('wihack', '-type', 'dialog', 'pavucontrol',
                        background=True),
    Match('RightBarMouseDown', 2, volume.name):
        lambda *a: pa_switcher(),
    Match('RightBarMouseDown', 3, volume.name):
        lambda *a: pactl('set-sink-mute 0 toggle'),
})

keys.bind('main', (
    ('XF86AudioRaiseVolume', 'Volume Up',
        lambda k: pactl('set-sink-volume 0 +5%')),
    ('XF86AudioLowerVolume', 'Volume Down',
        lambda k: pactl('set-sink-volume 0 -5%')),
    ('XF86AudioMute', 'Volume Toggle',
        lambda k: pactl('set-sink-mute 0 toggle')),
))
