import os


if(os.getenv("PYTHONPATH") == None):
    os.environ.setdefault("PYTHONPATH", os.getcwd())
else:
    os.environ["PYTHONPATH"] += ":"+os.curdir

from errors.login_fail import *
