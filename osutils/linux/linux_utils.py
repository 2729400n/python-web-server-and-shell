from sdd_constructs import *
import os
# Linux Utilities Only used on POSIX complaint Operating Systems

# Function for formating passwd like files no regexp all done by hand
# Files must be passed as bytes or str
#
# but sadly that also means it may not work for some Distros
# If Im running this on windows it doesnt matter


def format_passwd(r: "str|bytes"):
    if(r.__class__.lstrip("<class").rstrip(">").lstrip().strip("\"").strip("\'") == "bytes"):
        r = str(r, "ascii")
    _user_info_ = [str(), str(), str(), str(), str(), str(), str()]
    i = 0
    for p in r:
        if(p != ":"):
            _user_info_[i] += p
        else:
            i += 1
    user_info = {"username": _user_info_[0], "password": _user_info_[1], "uid": int(_user_info_[2]), "gid": int(
        _user_info_[3]), "uinfo": _user_info_[4].split(","), "home": _user_info_[5], "shell": _user_info_[6]}

    return user_info

# Function for getting a list of users with defined uids
#


def readusers(passwd_path="/etc/passwd"):
    f = open(passwd_path, "rt")
    users = dict()
    uids = []
    for i in f.readlines():
        backer = format_passwd(i)
        uid = backer["uid"]
        users.setdefault(uid, backer)
        uids.append(uid)
    f.close()
    return bubble_sort(uids), users


global UIDS, USERS
#UIDS, USERS = readusers()


def getuserInfoByUID(uid):
    return dict(USERS.get(uid))


def getuserByID(uid):
    return getuserInfoByUID(uid).get("username")


def getuidByUser(name: str):
    for i in USERS:
        if(name == USERS.get(i).get("username")):
            return int(USERS.get(i).get("uid"))


def getuserInfoByUser(name: str):
    getuserByID(getuidByUser(name))


del os
