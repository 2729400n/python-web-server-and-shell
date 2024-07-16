from email.mime import base
import os
import osutils.linux.linux_utils as posixutils

# Function finds a suitable directory containing the wanted file by searching recursivley through the basedir
# Then changes the CWD to the suitable directory


def search_for_suitable_directory(basedir: str = None, filename: str = None):
    # The basedir to begin searching from is a str that is a valid path
    # The filename to search for
    if(filename == None):
        filename = "index.html"
    if (basedir == None):
        basedir = os.getcwd()
    elif(not os.path.isdir(basedir)):
        basedir = os.curdir
    basedir = basedir.rstrip("/")
    suitable = -1
    search_paths = []
    directory_list = os.listdir(basedir)
    for i in directory_list:
        if suitable != 1:
            if(os.path.isdir("{1}/{0}".format(i, basedir)) & (not os.path.islink("{1}/{0}".format(i, basedir)))):
                search_paths.append(basedir+"/"+i)
            if(i == filename):
                suitable = 1
                search_paths.clear()
    if ((suitable != 1) & (suitable != 0)):
        for p in search_paths:
            # recursion because it takes to long the other way
            if((not os.path.islink(p)) and (suitable != 0)):
                suitable = search_for_suitable_directory(
                    p, filename)
    if(suitable == 1):
        os.chdir(basedir)
        print("cwd is {0}".format(os.getcwd()))
        return 0
    elif(suitable == 0):
        return 0
    return -1
