#!/usr/bin/env python

import urwid

palette = [('I say', 'default,bold', 'default', 'bold'),]

ask = urwid.Edit(('I say', "What is your name?\n"))
reply = urwid.Text("")
content = urwid.SimpleListWalker([ask, reply])
listbox = urwid.ListBox(content)

def on_ask_change(edit, new_edit_text):
    assert edit is ask # we are passed our edit widget
    reply.set_text(('I say',
        "Nice to meet you, " + new_edit_text))

urwid.connect_signal(ask, 'change', on_ask_change)

def exit_on_cr(input):
    if input == 'enter':
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(listbox, palette, unhandled_input=exit_on_cr)
loop.run()