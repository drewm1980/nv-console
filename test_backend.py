# Test cases for the backend
# call nosetests in same directory to run

import os
from nose.tools import *

toyDict = {'fruit':'apples\noranges\npears\npeaches\nraspberries\nstrawberries',
            'animals':'pythons\nbears\njellyfish\ndolphins\nelephants',
            'Sustainable Means of Transportation':'bicycling\nwalking\n'+\
            'taking the train',
            "A few of Drew's favorite things":'Stephanie Brabant\n'+\
            'python programming language\n'+\
            'bicycling\nstrawberries\n'}

def setup_func():
    import os
    os.system('rm -rf test')
    os.makedirs('test')

    from backend import *
    global db
    db = Database(location='test/notes',
                  encryptedLocation='test/.notes')

def teardown_func():
    os.system('rm -rf test')

@with_setup(setup_func, teardown_func)
def test_decrypt():
    db.load()
    
def test_database_sanity():
    hits = db.search('oran')
    assert hits==['fruit']
    body = db.get_body_from_title(hits[0])
    assert body == 'apples\noranges\npears\npeaches\raspberries\strawberries'
    print 'Database Sanity Test Passed!'
