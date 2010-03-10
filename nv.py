#!/usr/bin/python
# This is a urwid port of the Notational Velocity note taking program.
# Andrew Wagner 2010
import urwid

database = {'fruit':'apples\noranges\npears\npeaches\raspberries\strawberries',
            'animals':'pythons\nbears\njellyfish\ndolphins\nelephants',
            'Sustainable Means of Transportation':'bicycling\n\
            \nwalking\n\
            taking the train',
            "A few of Drew's favorite things":'python programming language\n\
            bicycling\nstrawberries\nnotational velocity\n'}

palette = [('filter', 'white', 'black'),
    ('list focus', 'black', 'dark cyan', 'standout'),
    ('list nofocus', 'black', 'dark gray'),
    ('body', 'black', 'white')]

# An Edit box for the filter
filterEdit = urwid.Edit("Filter?:", wrap='clip', multiline=False)
filterMap = urwid.AttrMap(filterEdit, 'filter')

# Temporary stand-in for what will probably be a listbox...
listText = urwid.Text('')
listMap = urwid.AttrMap(listText, 'list nofocus', 'list_focus')

# An Edit box for the body of the note
bodyEdit = urwid.Edit("Body?:")
bodyMap = urwid.AttrMap(bodyEdit, 'body')

def on_filter_change(widget, signal):
    assert widget == filterEdit
    assert type(signal) == str
    newString = signal
    listText.set_text('Got string: ' + newString)

urwid.connect_signal(filterEdit, 'change', on_filter_change)

pile = urwid.Pile([('fixed', 1, filterMap),
    ('weight',1,listMap),
    ('weight',2,bodyMap)], focus_item=filterMap)

def do_pass():
    pass

def do_quit():
    raise urwid.ExitMainLoop()

#loop = urwid.MainLoop(listbox, palette, unhandled_input=on_unhandled_input)
loop = urwid.MainLoop(pile, palette, unhandled_input=do_pass)

loop.run()