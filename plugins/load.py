from wmiirc import *

@defmonitor(interval=4, name='45-load')
def load(self):
    with open('/proc/loadavg') as f:
        l, m, s = f.read().split(' ')[:3]
        load = float(l)
        if load > 8:
            color = 'errorcolors'
        elif load > 4:
            color = 'noticecolors'
        elif load > 1:
            color = 'successcolors'
        else:
            color = 'normcolors'
        return wmii.cache[color], ' '.join((l, m, s))
