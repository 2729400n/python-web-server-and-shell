
from http.client import UnimplementedFileMode
import subprocess
import os

# Windows Utils


# Function for getting a list of users with defined uids
def readusers(cmd=["net", "user"]):
    users = []
    uinfo = dict()
    with subprocess.Popen(cmd, executable="net", stdout=-1, stdin=-1, stderr=-1, shell=True, universal_newlines=True, close_fds=False) as net_proc:
        users = net_proc.stdout.read().split()
        net_proc.terminate()
    for i in users:
        uinfo.setdefault(i, {"username": i, "shell": [
                         "runas", "/profile", "/user:127.0.0.1\\{0}".format(i), "cmd"]})

    return users, uinfo


global UIDS, USERS
#UIDS, USERS = readusers()


del os
