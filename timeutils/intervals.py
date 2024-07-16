import io
import time
import timeit
import threading
import tupleutils

global FUNC_FAILED, FUNC_HADNORESPONSE, FUNC_DOESNOTEXIST

FUNC_FAILED = -1
FUNC_DOESNOTEXIST = -1

global time_keeper, watcher, retvals, intervalIds
time_keeper = float()
retvals = dict()
watcher = dict()


def Timethread():
    pass


def caller(func, *args, timeinterval, amount, retaddr: "io.StringIO|io.FileIO|io.IOBase"):
    for i in range(0, amount):
        try:
            retaddr.seek(0)
            retaddr.write(func(args))
        except ReferenceError:
            return FUNC_DOESNOTEXIST
        except OSError:
            raise OSError


def setInterval(func: function, interval: "float|int"):
    watcher.setdefault(interval, {
                       "function": func, "interval": interval, "correction": time_keeper % interval})


def setTimeout(func: function, callback: function, time_interval: "float|int", retries=0, *args, **kwargs):
    retval = io.StringIO()
    args = (args)
    args = tupleutils.preppend(tupleutils.append(
        args, time_interval, retries, retval), func)
    thread = threading.Thread(
        None, caller, func.__name__, args, daemon=False)
    thread.start()
    thread.join()
    ret_pipe = retval.read()
    retval.close()
    return ret_pipe
