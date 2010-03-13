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

database = {'fruit':'apples\noranges\npears\npeaches\raspberries\strawberries',
            'animals':'pythons\nbears\njellyfish\ndolphins\nelephants',
            'Sustainable Means of Transportation':'bicycling\n\
            \nwalking\n\
            taking the train',
            "A few of Drew's favorite things":'python programming language\n\
            bicycling\nstrawberries\nnotational velocity\n'}

palette = [('search', 'white', 'black', '', 'black', 'g62'),
    ('list focus', 'black', 'dark cyan', '', 'black', '#8af'),
    ('list nofocus', 'black', 'dark gray', '', 'black', 'g78'),
    ('edit', 'black', 'white')]

verboseMode = True

# We will need text entries that are selectable later.
class SelectableText(urwid.Text):
    def selectable(self): return True
    def keypress(self, size, key):
        return key

# An Edit box for the filter
class NV_Edit1(urwid.Edit):        
    pass
if verboseMode:
    promptString = "Enter your search term here:"
else:
    promptString = ""
searchWidget = NV_Edit1(promptString, wrap='clip', multiline=False)

# A list walker for the filtered entries...
class NV_SimpleListWalker(urwid.SimpleListWalker):
    def selectable(self):
        return False
if verboseMode:
    promptString = "This area will contain filtered note titles \
once you start typing."
else:
    promptString = ""
listStrings = [promptString,'This is a second initial entry'+
                                ' for debugging purposes.']
listEntries = []
for s in listStrings:
    #listEntries.append(urwid.Text(s))
    listEntries.append(urwid.AttrMap(SelectableText(s),
                                     'list nofocus', 'list focus'))
listWidget = NV_SimpleListWalker(listEntries)

# An Edit for the body of the note...
# No need to subclass yet, but to be futureproof...
class NV_Edit2(urwid.Edit):        
    pass
if verboseMode:
    promptString = "This is where you view and edit notes:"
else:
    promptString = ""
editWidget = NV_Edit2(promptString, wrap='space', multiline=True,
                      allow_tab=True, edit_pos=0)

# A Pile to handle global keyboard focus...
class NV_Pile(urwid.Pile):
    def __init__(self, widget_list, focus_item=None):
        super(NV_Pile, self).__init__(widget_list, focus_item=None)
    def keypress(self, size, key):
        if key in ['ctrl q']:
            raise urwid.ExitMainLoop()
        if self.get_focus() == self.widget_list[1]:
            if key.lower() in ['tab']:
                self.set_focus(2)
            elif key.lower() in ['up','down','pageup','pagedown']:
                #listWidget.append(urwid.Text('first list entry got focus!'))
                key = self.widget_list[1].keypress(size, key)
                editWidget.set_edit_text(editWidget.get_edit_text()+
                                         '\nList focused on entry '+
                                         str(listWidget.get_focus()))
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
temp2 = urwid.AttrMap(temp2, 'list nofocus', 'list focus')

temp3 = editWidget
temp3 = urwid.AttrMap(temp3, 'edit')
temp3 = urwid.Filler(temp3,valign='top')

# Glue everything together
pile = NV_Pile([('flow', temp1),
    ('weight',1,temp2),
    ('weight',2,temp3)])

def on_unhandled_input(input=None):
    warn('Bug! Detected unhandled input:%s'%str(input))

loop = urwid.MainLoop(pile, palette, unhandled_input=on_unhandled_input)
loop.screen.set_terminal_properties(colors=256)
loop.run()

