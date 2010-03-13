#!/usr/bin/env python
import urwid

class SelectableText(urwid.Text):
    def selectable(self): return True
    def keypress(self, size, key):
        return key

palette = [('header', 'white', 'black'),
    ('reveal focus', 'black', 'dark cyan', 'standout'),]
content = urwid.SimpleListWalker([
    urwid.AttrMap(w, None, 'reveal focus') for w in [
    SelectableText("First Entry"),
    urwid.Divider("-"),
    SelectableText("Second Entry"),
    urwid.Divider("-"),
    SelectableText("Third Entry"),
    urwid.Divider("-"),
    SelectableText("Fourth Entry"),
    urwid.Divider("-"),
    SelectableText("Fifth Entry")]])
listbox = urwid.ListBox(content)

show_key = urwid.Text("", wrap='clip')
#head = urwid.AttrMap(show_key, 'header')
head = urwid.AttrMap(show_key, 'header', 'reveal focus')


top = urwid.Frame(listbox, head)

def exit_on_cr(input):
    if input == 'enter':
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(top, palette, unhandled_input=exit_on_cr)
loop.run()