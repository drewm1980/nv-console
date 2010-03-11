#!/usr/bin/env python

import urwid

palette = [('header', 'white', 'black'),
    ('reveal focus', 'black', 'dark cyan', 'standout'),]
content = urwid.SimpleListWalker([
    urwid.AttrMap(w, None, 'reveal focus') for w in [
    urwid.Text("This is a text string that is fairly long"),
    urwid.Divider("-"),
    urwid.Text("Short one"),
    urwid.Text("Another"),
    urwid.Divider("-"),
    urwid.Text("What could be after this?"),
    urwid.Text("The end."),]])
listbox = urwid.ListBox(content)
show_key = urwid.Text("", wrap='clip')
head = urwid.AttrMap(show_key, 'header')
top = urwid.Frame(listbox, head)

def show_all_input(input, raw):
    show_key.set_text("Pressed: " + " ".join([
        unicode(i) for i in input]))
    return input

def exit_on_cr(input):
    if input == 'enter':
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(top, palette,
    input_filter=show_all_input, unhandled_input=exit_on_cr)
loop.run()