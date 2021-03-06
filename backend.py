#!/usr/bin/env python
#
#    Copyright (C) 2011 Andrew Wagner
#   insert GPL here...

import os
from hashlib import md5
from config import *

class Database(object):
    def __init__(self, 
                 location='~/notes', 
                 encryptedLocation='~/.notes',
                 encryption='encfs'):
        encryptedLocation = os.path.expanduser(encryptedLocation)
        location = os.path.expanduser(location)
        encryptedLocation = os.path.abspath(encryptedLocation)
        location = os.path.abspath(location)
        self.notes = {}
        self.location = location;
        self.encryptedLocation=encryptedLocation
        self.encryption=encryption
    def load(self):
        if encryption == 'encfs':
            os.system('encfs --standard' + self.encryptedLocation 
                      + ' ' + self.location)
        self.filenames = os.listdir(self.location)
        for x in self.filenames:
            noteContents = open(os.path.join(self.location, x)).readlines()
            noteDescription = noteContents[0]
            try:
                noteBody = noteContents[1:]
            except IndexError:
                noteBody = ''
            self.notes[noteDescription] = noteBody
    def store_brutally(self):
        # Blow away all stored notes and write all im-memory notes
        rmcontents(self.location)
        for (noteDescription, noteBody) in self.notes.iteritems():
            filename = md5.new(noteDescription).hexdigest()
            fileContents = '\n'.join([noteDescription, noteBody])
            open(os.path.join(location, filename)).write(fileContents)
    def search(self, searchString):
        searchString = searchString.lower()
        returnKeys = []
        for (key,val) in self.notes.iteritems():
            lowerKey = key.lower()
            lowerVal = val.lower()
            if (lowerKey.find(searchString)>-1) or (lowerVal.find(searchString)>-1):
                returnKeys.append(key)
        return returnKeys
    def get_body_from_title(self,key):
        return self.notes[key]

