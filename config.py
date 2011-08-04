# This is the configuration file for nv-console.
# It uses python syntax.

encryptedDatabaseLocation = '~/.notes'
databaseLocation = '~/notes'
encryption = ['encfs','none'][0]

import os
encryptedDatabaseLocation = os.path.expanduser(encryptedDatabaseLocation)
databaseLocation = os.path.expanduser(databaseLocation)
