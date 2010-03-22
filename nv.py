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
class myEdit(urwid.Edit):
    def __init__(self, *argl, **argd):
        self.fakefocus = True
        return super(myEdit, self).__init__(*argl, **argd)
    def render(self, size, focus=False):
        return super(myEdit, self).render(size, self.fakefocus)

searchWidget = myEdit('', wrap='clip', multiline=False)

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
            else:
                key = self.widget_list[0].keypress((size[0],), key)
        elif self.get_focus() == self.widget_list[2]:
            if key.lower() in ['shift tab', 'tab']:
                self.set_focus(1)
                searchWidget.fakefocus = True
            else:
                key = super(NV_Pile, self).keypress(size, key)
        else:
            raise StandardError,"Oops! Pile focus reached an unexpected widget!"
        # Make sure the search widget fakefocus is still correct.
        searchWidget.fakefocus = self.get_focus()==self.widget_list[1]
    
    def mouse_event(self, size, event, button, col, row, focus):
        # Intercept clicks the search widget to keep focus on the list widget.
        if row==0:
            searchWidget.set_edit_pos(col)
            if self.get_focus() == self.widget_list[2]:
                self.set_focus(1)
        else:
            super(NV_Pile, self).mouse_event(size, event, button, col, row, focus)
        # Make sure the search widget fakefocus is still correct.
        searchWidget.fakefocus = self.get_focus()==self.widget_list[1]

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
    assert type(sourceWidget)==myEdit, 'I was expecting a myEdit widget!'
    assert type(listWidget)==urwid.SimpleListWalker, "listWidget is not the "+\
                                                    "expected type!!"
    (focusWidget, focusPosition) = listWidget.get_focus()
    if focusWidget==None:
        previouslySelectedKey = None
    else:
        previouslySelectedKey = focusWidget.original_widget.text
    
    # The top Edit box search string has changed.
    listStrings = db.search(searchString)  # Should be mixed case.
    listEntries = []
    for s in listStrings:
        listEntries.append(urwid.AttrMap(SelectableText(s),
                                             'list nofocus', 'list focus'))
        
    # Treat the SimpleListWalker like a list...    
    del listWidget[:]
    listWidget.extend(listEntries)

    # Keep list focus stable, and update body edit window if necessary    
    if previouslySelectedKey in listStrings:
        listWidget.set_focus(listStrings.index(previouslySelectedKey))
    elif len(listStrings)>0:
        listWidget.set_focus(0)
        editWidget.set_edit_text(db.get_body_from_title(listStrings[0]))
urwid.connect_signal(searchWidget, 'change', on_search_update)

def on_list_focus_change():
    (focusWidget, focusPosition) = listWidget.get_focus()
    if focusWidget==None:
        editWidget.set_edit_text('')
    else:
        newSelectedKey = focusWidget.original_widget.text
        editWidget.set_edit_text(db.get_body_from_title(newSelectedKey))
urwid.connect_signal(listWidget, 'modified', on_list_focus_change)

def on_unhandled_input(input=None):
    warn('Bug! Detected unhandled input:%s'%str(input))

loop = urwid.MainLoop(pile, palette, unhandled_input=on_unhandled_input)
loop.screen.set_terminal_properties(colors=256)
loop.run()

