# This is just a place to hold non-functional code bits.

def on_filter_change(filterEdit, searchString):
    global listListBox
    # search the titles of the dictionary keys
    foundKeys = [k for k in database.iterkeys() if k.find(searchString)>-1]
    listListBox.extend(string_to_list_box(foundKeys))

urwid.connect_signal(filterEdit, 'change', on_filter_change)


            if key=='up':
                listBox._keypress_up(size)
            elif key=='down':
                listBox._keypress_down(size)
            elif key=='pageup':
                listBox._keypress_pageup(size)
            elif key=='pagedown':
                listBox._keypress_pagedown(size)

