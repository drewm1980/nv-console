#!/usr/bin/python

import urwid

ask = urwid.Edit("What is your name?\n")
fill = urwid.Filler( ask )

def do_reply(input):
    if input != 'enter':
        return
    if fill.body == ask:
        fill.body = urwid.Text( "Nice to meet you,\n"+
            ask.edit_text+"." )
    else:
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(fill, unhandled_input=do_reply)
loop.run()
