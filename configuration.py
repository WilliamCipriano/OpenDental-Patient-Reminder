import sys
import os

#This loads the config.ini file from the hard drive and uses those to contact twillio, this code can be reused in other projects rather easily.

try:
    path = os.path.dirname(os.path.abspath(__file__)).replace('\\library.zip','')
except NameError:  # We are the main py2exe script, not a module
    import sys
    path = os.path.dirname(os.path.abspath(sys.argv[0])).replace('\\library.zip','')

config = open(path + '\config.ini')
config = config.read()
config = config.split('\n')
x = 0
for line in config:
    if x == 0:
        SID = line
        SID = SID.split('= ')
        SID = SID[1]
    elif x == 1:
        AUTH = line
        AUTH = AUTH.split('= ')
        AUTH = AUTH[1]
    elif x == 2:
        NUMBER = line
        NUMBER = NUMBER.split('= ')
        NUMBER = NUMBER[1]
    x += 1


def sid():
    return SID


def auth():
    return AUTH


def number():
    return NUMBER
