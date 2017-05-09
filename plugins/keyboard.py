from wmiirc import *
import re
import os
import threading

defaults = ['us', 'de', 'es', 'fr', 'gb', 'in']

@defmonitor(interval=60, name='91-keyboard')
def keyboard(self):
    query = call('setxkbmap', '-query')
    info = dict(map(str.strip, ln.split(':')) for ln in query.strip().split('\n'))
    return wmii.cache['normcolors'], u'[:%s:]' % info.get('layout', '--')

def keyboard_set(layout):
  def set():
    call('setxkbmap', layout, background=False)
    keyboard.tick()
  return set

def keyboard_menu():
  clickmenu([(layout, keyboard_set(layout)) for layout in defaults], [])

events.bind({
    Match('RightBarMouseDown', 3, keyboard.name): lambda *a: keyboard_menu()})
