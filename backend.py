#!/usr/bin/env python
#
#    Copyright (C) 2010 Andrew Wagner
#   insert GPL here...
class Database(object):
    def __init__(self, initialDict={}):
        self.notes = initialDict
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

toyDict = {'fruit':'apples\noranges\npears\npeaches\nraspberries\nstrawberries',
            'animals':'pythons\nbears\njellyfish\ndolphins\nelephants',
            'Sustainable Means of Transportation':'bicycling\nwalking\n'+\
            'taking the train',
            "A few of Drew's favorite things":'Stephanie Brabant\n'+\
            'python programming language\n'+\
            'bicycling\nstrawberries\n'}

def test_database_sanity():
    db = Database(toyDict)
    hits = db.search('oran')
    assert hits==['fruit']
    body = db.get_body_from_title(hits[0])
    assert body == 'apples\noranges\npears\npeaches\raspberries\strawberries'
    print 'Database Sanity Test Passed!'

if __name__=='__main__':
    test_database_sanity()