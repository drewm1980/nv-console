#!/usr/bin/python
# This is a urwid port of the Notational Velocity note taking program.
# Andrew Wagner 2010
import urwid

filterEdit = urwid.Edit("This is the filter text.", wrap='clip')
filterFiller = urwid.Filler( filterEdit )

def do_reply(input):
    if input != 'enter':
        return
    if filterFiller.body == ask:
        filterFiller.body = urwid.Text( "Filter text is...\n"+
            ask.edit_text )
    else:
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(filterFiller, unhandled_input=do_reply)
loop.run()