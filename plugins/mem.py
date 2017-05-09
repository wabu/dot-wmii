from wmiirc import *

@defmonitor(interval=4, name='44-mem')
def mem(self):
    with open('/proc/meminfo') as f:
	info = {key: float(val.strip().replace(' kB', ''))
                for key, val in map(lambda x: x.split(':'), f.read().strip().split('\n'))}
     
        total = info['MemTotal']
        #free = info['MemFree']
        avail = info['MemAvailable']
        #buff = info['Buffers']
        #cached = info['Cached'] + info['SwapCached']

        swap = (info['SwapTotal'] - info['SwapFree']) / (info['SwapTotal'] + 1e-9)

        #out = ('\%02d\%02d,%02d,%02d/%02d/' % 
        #       tuple(map(lambda x: (x/total*100), [avail, free, buff, cached, swap])))
        out = '|%02d|%02d|' % ((total-avail)/total*100, swap*100)

        if avail/total < .1:
            color = 'errorcolors'
        elif avail/total < .2:
            color = 'noticecolors'
        else:
            color = 'normcolors'
        return wmii.cache[color], out
