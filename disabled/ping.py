from wmiirc import *
import os

history = []

@defmonitor(name='86-ping', interval=5)
def ping(self):
    ok = os.system('ping -W2 -c1 109.239.49.244 > /dev/null 2>&1') == 0

    history.append(ok)
    if len(history) > 100:
        history.pop(0)

    long = float(sum(history)) / len(history)
    short = float(sum(history[-10:])) / len(history[-10:])

    if long == 1:
        color = 'normcolors'
    elif short == 1:
        color = 'successcolors'
    elif ok and short > long:
        color = 'focuscolors'
    else:
        color = 'noticecolors'

    if short > long + 0.02:
        trend = '^'
    elif short < long - 0.02:
        trend = 'v'
    else:
        trend = '~'

    if long == 1:
        msg = '..'
    else:
        msg = '.%d%s%d.' % (long*10,trend,short*10)

    return wmii.cache[color], msg

