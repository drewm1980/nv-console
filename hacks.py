import os

def rmcontents(path):
    for root, dirs, files in os.walk(self.location):
        for f in files:
            fullpath = os.path.join(root, f)
            os.remove(fullpath)
