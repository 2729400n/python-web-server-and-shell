import os


if(os.getenv("PYTHONPATH") == None):
    os.environ.setdefault("PYTHONPATH", os.getcwd())
else:
    os.environ["PYTHONPATH"] += ":"+os.curdir

global osnames
osnames = {"posix": False, "nt": False}
if os.name in osnames:
    # defines functions for sorting out posixs compications
    # might make one for windows
    osnames[os.name.lower()] = True

if(osnames["posix"]):
    import osutils.linux.linux_utils as utils
elif(osnames["nt"]):
    import osutils.windows.windows_utils as utils
del os
