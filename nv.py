#!/usr/bin/python
# This is an urwid port of the Notational Velocity note taking program.
# Andrew Wagner 2010
import urwid

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

# An Edit box for the filter
class NV_Edit1(urwid.Edit):        
    def keypress(self, size, key):
        # Filter out Up and down arrows and send them to the ListBox.
        if key in ['up','down']:
            searchList.keypress(size, key)
        else:
            super(NV_Edit1, self).keypress(size, key)
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
listWidget = NV_SimpleListWalker([urwid.Text(promptString)])

# An Edit for the body of the note...
# No need to subclass yet, but to be futureproof...
NV_Edit2 = urwid.Edit
if verboseMode:
    promptString = "This is where you view and edit notes:"
else:
    promptString = ""
editWidget = NV_Edit2(promptString, wrap='space', multiline=True)

# A Pile to handle global keyboard focus...
class NV_Pile(urwid.Pile):
    def __init__(self, widget_list, focus_item=None):
        super(NV_Pile, self).__init__(widget_list, focus_item=None)
    def keypress(self, size, key):
        if key in ['Ctrl-Q']:
            raise urwid.ExitMainLoop()
        if self.get_focus() == 0:
            if key.lower() in ['tab']:
                self.set_focus(2)
            else:
                return super(NV_Pile, self).keypress(size, key)
        elif self.get_focus == 2:
            if key.lower() in ['shift-tab']:
                self.set_focus(0)
            else:
                return super(NV_Pile, self).keypress(size, key)

# Add some formatting and padding widgets.
temp1 = searchWidget
temp1 = urwid.AttrMap(temp1, 'search')

temp2 = listWidget
temp2 = urwid.ListBox(temp2)
temp2 = urwid.AttrMap(temp2, 'list nofocus', 'list_focus')

temp3 = editWidget
temp3 = urwid.AttrMap(temp3, 'edit')
temp3 = urwid.Filler(temp3)

# Glue everything together
pile = NV_Pile([('flow', temp1),
    ('weight',1,temp2),
    ('weight',2,temp3)])

def do_pass():
    pass

loop = urwid.MainLoop(pile, palette, unhandled_input=do_pass)
loop.screen.set_terminal_properties(colors=256)
loop.run()




#def on_filter_change(filterEdit, searchString):
#    global listListBox
#    # search the titles of the dictionary keys
#    foundKeys = [k for k in database.iterkeys() if k.find(searchString)>-1]
#    listListBox.extend(string_to_list_box(foundKeys))

#urwid.connect_signal(filterEdit, 'change', on_filter_change)

