from pygmi import *
from wmiirc import *

background = '#eee8d5'
floatbackground='#bbe85'

wmii['font'] = 'xft:Fira Code:pixelsize=9'
wmii['fontpad'] = '0 0 -1 -1'.split()


wmii['normcolors'] = "#4A4A7A #EEEEEF #DADAEA".split()
wmii['focuscolors'] = "#3A3A6A #CECEDE #5A5A8A".split()

wmii['errorcolors'] = "#EF0020 #FBD3E4 #FF0020".split()
wmii['noticecolors'] = "#514721 #FFF6BF #FFD324".split()
wmii['successcolors'] = "#264409 #E6EFE2 #B6D870".split()

wmii['border'] = 1


@defmonitor(name='00-nil', interval=0)
def nil(self):
    return wmii.cache['normcolors'], ' '


@defmonitor(name='94-date', interval=60)
def date(self):
    return (wmii.cache['focuscolors'],
            datetime.datetime.now().strftime('%a %d.%m'))

@defmonitor(name='95-time', interval=10)
def time(self):
    n = wmii.cache['normcolors']
    f = wmii.cache['focuscolors']
    return ([n[0], n[1], f[2]],
            datetime.datetime.now().strftime('%H:%M'))

events.bind({
    Match('RightBarMouseDown', 3, time.name): lambda *a: clickmenu((
            ('Lock',   lambda: call('slimlock', background=True)),
            ('Suspend',lambda: call('sudo', 'hibernate-ram', background=True)),
            ('Reload', lambda: call('%s/wmiirc' % confpath[0], background=True)),
            ('Logout', lambda: wmii.ctl('quit')),
        ), ()),
    Match('RightBarMouseDown', 2, '46-thermal'): lambda *a: wmii.toggle_thermal(),
    Match('RightBarClick', 4, _): lambda *a: tags.select(tags.next(True)),
    Match('RightBarClick', 5, _): lambda *a: tags.select(tags.next()),
    Match('ClientMouseDown', _, 3): lambda e, client, n: clickmenu((
            ('[%s|%s]' % tuple(Client(client).props.split(':')[:2]), lambda c: True),
            ('Delete',     lambda c: Client(c).kill()),
            ('Slay',       lambda c: Client(c).slay()),
            ('Fullscreen', lambda c: Client(c).set('Fullscreen', 'on')),
        ), (client,)),
    #Match('ACPI', 'button/lid', 'LID', 'close'): lambda *a: call(
    #    'slimlock', background=True),
    Match('ACPI', 'button/sleep'): lambda *a: call(
        'slimlock', background=True),
    Match('ACPI', 'button/hibernate'): lambda *a: call(
        'slimlock', background=True),
})

tags.ignore.add(u'|')


keys.bind('main', (
    ('%(mod)s-x', "Launch a terminal",
         lambda k: call(*terminal, background=True)),
    ('%(mod)s-Return', "Launch terminal on deukalion",
         lambda k: call('urxvt', '-e', 'ssh', '-AtY', 'deukalion', background=True)),
    ('%(mod)s-BackSpace', "Select overlay view",
         lambda k: tags.select('|') if tags.sel != tags.tags.get('|') else tags.select(tags.before)),
    ('%(mod)s-grave', "Select 'net' view",
         lambda k: tags.select('net') if tags.sel != tags.tags['net'] else tags.select(tags.before)),
    ('%(mod)s-Delete', "Lock the screen",
         lambda k: call('dm-tool', 'lock')),
    ('%(mod)s-q', "Close client",
         lambda k: Client('sel').kill()),
    ('%(mod)s-Tab', "Switch to tag selected before",
         lambda k: tags.select(tags.before)),
    ('XF86ScreenSaver', "Lock the screen",
         lambda k: call('slimlock', background=True)),
    ('XF86WLAN', "Be Quiet",
         lambda k: wmii.toggle_thermal()),
    ('XF86MonBrightnessUp', "Brightness Up",
         lambda k: call('xbacklight', '+10%', background=True)),
    ('XF86MonBrightnessDown', "Brightness Down",
         lambda k: call('xbacklight', '-10%', background=True)),
))

def binding(i):
    return ('%%(mod)s-%d' %i, 'Move to %dth view' % i,
            lambda k: tags.select(tags.nth(i)))
keys.bind('main', tuple([binding(i) for i in range(10)]))

wmii.ctl('bar on top')
for name in wmii.tags:
    tag = tags.tags[name]
    color = 'focuscolors' if tags.sel == tag else 'normcolors'
    tag.button.colors = wmii.cache[color]
