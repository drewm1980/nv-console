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

palette = [('filter', 'white', 'black', '', 'black', 'g62'),
    ('list focus', 'black', 'dark cyan', '', 'black', '#8af'),
    ('list nofocus', 'black', 'dark gray', '', 'black', 'g78'),
    ('body', 'black', 'white')]

# An Edit box for the filter
filterEdit = urwid.Edit("", wrap='clip', multiline=False)
filterMap = urwid.AttrMap(filterEdit, 'filter')

# Temporary stand-in for what will probably be a listbox...
def string_to_list_box(strings):
    listEntries = [urwid.Text(s) for s in strings]
    listEntries2 = [urwid.AttrMap(e, 'list nofocus', 'list_focus') for e in listEntries]
    listContent = urwid.SimpleListWalker(listEntries2)
    listListBox = urwid.ListBox(listContent)
    return listListBox

listListBox = string_to_list_box(['initial', 'values'])
#listFiller = urwid.Filler(listListBox, valign='top')
#listMap = urwid.AttrMap(listListBox, 'list nofocus', 'list_focus')

# An Edit box for the body of the note
bodyEdit = urwid.Edit("", wrap='space', multiline=True)
bodyFiller = urwid.Filler(bodyEdit, valign='top')
bodyMap = urwid.AttrMap(bodyFiller, 'body')

def on_filter_change(filterEdit, searchString):
    global listListBox
    # search the titles of the dictionary keys
    foundKeys = [k for k in database.iterkeys() if k.find(searchString)>-1]
    listListBox.extend(string_to_list_box(foundKeys))

urwid.connect_signal(filterEdit, 'change', on_filter_change)

pile = urwid.Pile([('flow', filterMap), # filter computes its own height (1)
    ('weight',1,listListBox),
    ('weight',2,bodyMap)], focus_item=filterMap)

def do_pass():
    pass

def do_quit():
    raise urwid.ExitMainLoop()

#loop = urwid.MainLoop(listbox, palette, unhandled_input=on_unhandled_input)
loop = urwid.MainLoop(pile, palette, unhandled_input=do_pass)
loop.screen.set_terminal_properties(colors=256)
loop.run()