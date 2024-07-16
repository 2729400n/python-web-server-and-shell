import os

if(os.getenv("PYTHONPATH") == None):
    os.environ.setdefault("PYTHONPATH", os.getcwd())
else:
    os.environ["PYTHONPATH"] += ":"+os.curdir

from httputils.http_format import *

del os
