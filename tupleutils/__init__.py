import os

if(os.getenv("PYTHONPATH") == None):
    os.environ.setdefault("PYTHONPATH", os.getcwd())
else:
    os.environ["PYTHONPATH"] += ":"+os.curdir

from tupleutils.workarounds import *

del os
