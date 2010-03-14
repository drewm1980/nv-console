#!/usr/bin/python
# This is an urwid port of the Notational Velocity note taking program.
# Andrew Wagner 2010
from warnings import warn
from time import sleep
try:
    import urwid
except ImportError:
    raise ImportError, "Oops, Notational Velociy could not find the urwid"+\
                        "library!  On Debian, try something like:"+\
                        "# apt-get install urwid"
expectedUrwidVersion = '0.9.9.1'
assert urwid.__version__ >= '0.9.9', 'Sorry, you need a newer version of '+\
                            'urwid. Please update.  If you''re on Debian, '+\
                            'try the version in the testing branch.'
if urwid.__version__!=expectedUrwidVersion:
    warn('This code was written for urwid version %s, but version %s was '+
         'found.\nGood luck!')%(expectedUrwidVersion, urwid.__version__)
    sleep(1)

import backend

# For now, just work with a toy dictionary.
db = backend.Database(backend.toyDict)

palette = [('search', 'white', 'black', '', 'black', 'g62'),
    ('list focus', 'black', 'light gray', '', 'black', 'g78'),
    ('list nofocus', 'black', 'dark gray', '', 'black', 'g70'),
    ('edit', 'black', 'white')]

# We will need text entries that are selectable later.
class SelectableText(urwid.Text):
    def selectable(self): return True
    def keypress(self, size, key):
        return key

# An Edit box for the filter
searchWidget = urwid.Edit('', wrap='clip', multiline=False)

# A list walker for the filtered entries...
listStrings = db.search('')
listEntries = []
for s in listStrings:
    listEntries.append(urwid.AttrMap(SelectableText(s),
                                     'list nofocus', 'list focus'))
listWidget = urwid.SimpleListWalker(listEntries)

# An Edit for the body of the note...
editWidget = urwid.Edit('', wrap='space', multiline=True,
                      allow_tab=True, edit_pos=0)

# A Pile to handle global keyboard focus...
class NV_Pile(urwid.Pile):
    def __init__(self, widget_list, focus_item=None):
        super(NV_Pile, self).__init__(widget_list, focus_item=1)
    def keypress(self, size, key):
        if key in ['ctrl q']:
            raise urwid.ExitMainLoop()
        if self.get_focus() == self.widget_list[1]:
            if key.lower() in ['tab']:
                self.set_focus(2)
            elif key.lower() in ['up','down','pageup','pagedown']:
                key = self.widget_list[1].keypress(size, key)
                return key
            else:
                return self.widget_list[0].keypress((size[0],), key)
        elif self.get_focus() == self.widget_list[2]:
            if key.lower() in ['shift tab']:
                self.set_focus(1)
            else:
                return super(NV_Pile, self).keypress(size, key)
        else:
            raise StandardError,"Oops! Pile focus reached an unexpected widget!"

# Add some formatting and padding widgets.
temp1 = searchWidget
temp1 = urwid.AttrMap(temp1, 'search')

temp2 = listWidget
temp2 = urwid.ListBox(temp2)
listBox = temp2
temp2 = urwid.AttrMap(temp2, 'list nofocus', 'list nofocus')

temp3 = editWidget
temp3 = urwid.AttrMap(temp3, 'edit')
temp3 = urwid.Filler(temp3,valign='top')

# Glue everything together
pile = NV_Pile([('flow', temp1),
    ('weight',1,temp2),
    ('weight',2,temp3)])

def on_search_update(sourceWidget, searchString):
    assert type(sourceWidget)==urwid.Edit, 'I was expecting an urwid.Edit!'
    assert type(listWidget)==urwid.SimpleListWalker, "listWidget is not the "+\
                                                    "expected type!!"
    (focusWidget, focusPosition) = listWidget.get_focus()
    if focusWidget==None:
        previouslySelectedKey = None
    else:
        previouslySelectedKey = focusWidget.original_widget.text
    
    # The top Edit box search string has changed.
    listStrings = db.search(searchString)
    listEntries = []
    for s in listStrings:
        listEntries.append(urwid.AttrMap(SelectableText(s),
                                             'list nofocus', 'list focus'))
        
    # Treat the SimpleListWalker like a list...    
    del listWidget[:]
    listWidget.extend(listEntries)
    
urwid.connect_signal(searchWidget, 'change', on_search_update)


def on_unhandled_input(input=None):
    warn('Bug! Detected unhandled input:%s'%str(input))

loop = urwid.MainLoop(pile, palette, unhandled_input=on_unhandled_input)
loop.screen.set_terminal_properties(colors=256)
loop.run()

