#!/usr/bin/env python3
import os

from click import FileError
from errors import login_fail
if(os.getenv("PYTHONPATH") == None):
    os.environ.setdefault("PYTHONPATH", os.getcwd())
import http.server
import threading
import sys
import re
import socket
import errno
import socketserver
from errors import *

import io
import json
from httputils import *
from sessionmanagment import *
from linux_utils import *
# For Keyboard Utils
import turtle
# My library for formating php
import format
import http.client
import http
import subprocess
import time

# Cryptographic libraries
if(os.name!='nt'):
    import crypt
else :
    crypt=None
#import cryptography.hazmat.primitives.ciphers.algorithms as crptoalgs
from sessionmanagment.sessionkey import make_new_key
from fsutils import *

# Check if the os is supports posixs operations
# If so imports my Posixs library

# Uncomment imports for more specialised control and better quality server with optimizations such as compression with gzip or base 64
# Migth make these a comand line option
# import gzip
# import base64
# import math


# Uncomment imports and add your own code to use them
# if you want to add audio support uncomment ossaudiodev
# If You want to add sql Date fromat for interacting with sql servers uncomment sqlite3 line but you will need to add
# a method for implementing the sql server connect
#
#	import html.parser
#	import ossaudiodev
#	from sqlite3 import Date

# The Default error response for errors
err_response = "<!DOCTYPE HTML>\n<html><head><title>NOT FOUND</title></head><body><h1>NOT FOUND</h1><p>The File or Resource Requested was not found</p><a href=\"/\"><img src=\"../goback.png\"</body></html>"
# Its length for sending through sockets
err_len = len(err_response)

# The class that handles the socket sid of things inherits from socket as well and threading very clustered


class HTTPSERVER(socket.socket):
    # Member Variable/fields/properties depends on the person really

    # For socket management it is an array which holds 2 dictionaries and an intger that is equal to the number of active Connection
    # The first stores the socket object of the peer
    # The second stores its connecting address as a tuple
    # The third stores the properties of the connection like if it alive or not
    activesockets = [{}, {}, {}, 0]

    # the active count of sockets connected for backing May be removed serves no purpose
    activecount = 0

    # A dictionary that holds the active shell sessions the key is set to a hash of somekind
    shellsessions = dict()

    # A boolean that is set to false at max connection capacity to prevent ddos attacks but limits amount of connectors
    connectionopen = True

    # Another boolean for backing used in debug phase
    allowing_connections = True

    # Holds the thread Object used to call run but then can't be used again so once request is finished the thread object is removed from the dictionary
    # THe key for indexing is the peeraddr where the ipaddress and port are seperated by a ":" (colon)
    activerequests = dict()

    # A dictionary because its easier but stores the key to the other dictionaries the key is the priority of connection
    sessionids = dict()

    # stores the amount of threads used-1
    currentamount = 0

    # stores the allowed amount of threads can be useful for connections that create multiple threads
    allowedamount = int()

    # A socket that allows for someone to debug the running process remotley
    # Not implemented yet
    debugsocket = None
    
    # End socket
    #Dont worry its been fixed
    close_sock = False

    # Methods

    # The constructor method
    # initialises the activesockets array in a for loop
    # makes sure the connections amount is set to 0
    # then uses the super constructor method to initialise the Object
    # Has a sapce for setting the request handler if you have a special protocol or set of things you are using it for

    def __init__(self, requesthandler=http.server.SimpleHTTPRequestHandler.__init__) -> None:
        self.requesthandler = requesthandler
        for i in [0, 1, 2, 3]:
            if i < 3:
                self.activesockets[i] = dict()
            else:
                self.activesockets[i] = 0
            super().__init__(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)

    def process_request(self):
        f = self.recv(65535)
        return f

    def accept(self) -> "tuple[socket.socket, tuple[str,int]]":
        conn, addr = super().accept()
        self.activesockets[0].setdefault(
            "{0}:{1}".format(addr[0], addr[1]), conn)
        self.activesockets[1].setdefault(
            "{0}:{1}".format(addr[0], addr[1]), addr)
        self.activesockets[2].setdefault("{0}:{1}".format(
            addr[0], addr[1]), {"alive": True, "JRAR": True, "lastsent": 9999})
        self.activesockets[3] += 1
        self.activecount += 1
        return (conn, addr)

    def listen(self, __backlog=0) -> None:
        if(self.getsockname()[1] == 0):
            try:
                self.bind(("0.0.0.0", 80))
            except Exception as e:
                try:
                    self.bind(("0.0.0.0", 8080))
                except:
                    self.bind(("0.0.0.0", 0))

        print("Listening on port {0}".format(self.getsockname()[1]))
        if(__backlog & __backlog >= 1):
            self.allowedamount = __backlog
        else:
            self.allowedamount = 9000

        for i in range(0, self.allowedamount):
            self.sessionids.setdefault(i, None)
        return super().listen(__backlog)

    def handlerequests(self, sessionid, placement):
        self.activesockets[0][sessionid].settimeout(9000)
        while (self.activesockets[2][sessionid]["alive"]==True):
            f=""
            try:
                while f =="":
                    f = str(self.activesockets[0][sessionid].recv(2048), 'iso-8859-1')
                print(f)
                req = f.split("\n")[0]
                reqfl = req.rstrip("\r").strip("\n").strip("\r")
                reqal = f.split("\r\n")
                reqal.pop(0)
                reqfl = reqfl.split()
                req = req.lower()
                response_file = None
                finished = False
                __vars__ = dict()

                try:
                    if("HTTP/" in reqfl[2]):   
                        if(reqfl[0].upper() == "GET"):
                            if("HTTP/" in reqfl[2]):
                                response = "%s %d %s\r\n" % (reqfl[2], 200, "OK")
                                response += "Date:{0}\r\n".format(
                                    local_http_time())
                                response += "Server: KevsPythonServer\r\n"
                                if((reqfl[1][len(reqfl[1])-1] != "/") & (os.path.isdir(reqfl[1]) != True)):
                                    response_file = open("./{0}".format(reqfl[1].lstrip("/")), "rb")
                                else:
                                    response_file = open("./{0}".format("index.html"), "rb")
                                response_file.seek(0)
                                body = b'\r\n' + response_file.read()+b'\r\n' # body = b'\r\n' + response_file.read(int(str(fstat).split(",")[6].strip().strip("st_size=").strip()))+b'\r\n'
                                fstat = os.fstat(response_file.fileno())
                                st_mtime = str(fstat).split(",")[8].strip().strip("st_mtime=").strip()
                                response_file.close()
                                response += "Last-Modified:{0}\r\n".format(local_http_time(st_mtime))
                                # .format(str(fstat).split(",")[6]strip().strip("st_size=").strip())
                                response += "Content-Length:cl_tbc\r\n"
                                if(".html" in response_file.name):
                                    response += "Content-Type: text/html"
                                elif(".js" in response_file.name):
                                    response += "Content-Type: text/javascript"
                                elif(".ico" in response_file.name):
                                    response += "Content-Type: image/x-icon"
                                elif(".css" in response_file.name):
                                    response += "Content-Type: text/css; charset=UTF-8"
                                else:
                                    response += "Content-Type: text/plain"
                                if('keep-alive'.lower() not in req.lower()):
                                    response += "\r\nConnection: Closed\r\n"
                                else:
                                    response += "\r\nConnection: Closed\r\n"
                                " ".join(response)

                                response.replace("cl_tbc", "{0}".format(len(body)))
                                response = bytes(response, 'iso-8859-1')
                                # print(str(body,'iso-8859-1'))
                                self.activesockets[0][sessionid].send(response)
                                self.activesockets[0][sessionid].send(body)
                                #if('Closed'.lower() in req.lower()):
                                self.activesockets[0][sessionid].close()
                                #if('Closed'.lower() in req.lower()):
                                self.activesockets[2][sessionid]["alive"] = False
                        elif(reqfl[0]== "POST"):
                            if "/shell" in reqfl:
                                shellreq = b''
                                for i in reqal:
                                    if((":" not in i)&(i!=None)&(i!="")):
                                        varset = i.split("&")
                                        for ii in varset:
                                            key, value = ii.split("=", 1)
                                            __vars__.setdefault(key.strip(), value.strip())
                                    elif("cookie" in i.lower()):
                                        i = i.split(":",1)[1]
                                        varset = i.split(";")
                                        for ii in varset:
                                            key, value = ii.split("=", 1)
                                            __vars__.setdefault(key.strip(), value.strip())
                                if((__vars__.get("sessionkey") != None)&(__vars__.get("sessionkey") in self.shellsessions)):
                                    args = __vars__["args"].split(",")
                                    command: "list[str]" = [__vars__["command"]]
                                    for i in args:
                                        command.append(i)
                                    proc: subprocess.Popen = self.shellsessions[__vars__[
                                        "sessionkey"]]["proc"]
                                    finished = False
                                    proc.stdin.write("\x20".join(command))
                                    proc.stdout.flush()
                                    #if shell_req != b'':
                                        # proc.communicate(shell_req)
                                    response = "%s %d %s\r\n" % (reqfl[2], 200, "OK")
                                    response += "Date:{0}\r\n".format(local_http_time())
                                    response += "Server: KevsPythonServer\r\n"
                                    response += "Last-Modified:{0}\r\n".format(local_http_time(0))
                                    response_file = "output={0};errorout={1};status=continue".format(proc.stdout.read(),proc.stderr.read())
                                    print(response_file)
                                    response += "Content-Length:{0}\r\n".format(len(response_file))
                                    response += "Content-Type: text/plain"
                                    response += "\r\nConnection: Keep-alive\r\n"
                                    " ".join(response)
                                    if(proc.returncode!=None):
                                        finished=True
                                    self.activesockets[0][sessionid].send(response)
                                    if(proc.returncode!=None):
                                        pass
                                    else:
                                        self.activesockets[0][sessionid].send("output={0};status=continue".format(response_file))
                                    if(proc.returncode!=None): 
                                        self.activesockets[0][sessionid].close()
                                else:
                                    response = "%s %d %s\r\n" % (reqfl[2], 404, "OK")
                                    response += "Date:{0}\r\n".format(local_http_time())
                                    response += "Server: KevsPythonServer\r\n"
                                    response += "Last-Modified:{0}\r\n".format(local_http_time(0))
                                    response_file = err_response
                                    response += "Content-Length:{0}\r\n".format(len(response_file))
                                    response += "Content-Type: text/plain"
                                    response += "\r\nConnection: Closed\r\n"
                                    self.activesockets[0][sessionid].send(response)
                                    self.activesockets[0][sessionid].send("output=You Are not logged In;errorout:login failed;status=continue;do_login=true;")
                                    self.activesockets[0][sessionid].close()

                            elif "/login" in reqfl:
                                #req = str(self.activesockets[0][sessionid].recv(6553), encoding='iso-8859-1')
                                print(bytes(req, 'iso-8859-1'))
                                print(reqal)
                                for i in reqal:
                                    if((":" not in i) and ("&" in i)):
                                        varset = i.split("&")
                                        for ii in varset:
                                            key, value = ii.split("=", 1)
                                            try:
                                                __vars__.setdefault(key.strip(), value.strip())
                                            except Exception as excep:
                                                print(excep)
                                    elif("cookie" in i.lower()):
                                        i = i.split(":",1)[1]
                                        varset = i.split(";")
                                        for ii in varset:
                                            key, value = ii.split("=", 1)
                                            __vars__.setdefault(key.strip(), value.strip())

                                if (self.shellsessions.get(__vars__.get("sessionkey")) == None) | (self.shellsessions.get("sessionkey") == None):
                                    sessionkey = ""
                                    salt = crypt.mksalt()
                                    sessionkey = crypt.crypt(sessionid, salt)
                                    self.shellsessions.setdefault(sessionkey, {"sessionkey": crypt.crypt(sessionid, salt), "proc": subprocess.Popen(getuserInfoByUser(__vars__.get("user",__vars__.get("username"))).get("shell"), universal_newlines=True , stdin=-1,stdout=-1,stderr=-1,close_fds=False), "sessionid": sessionid})
                                    del salt

                                try:
                                    if ((__vars__.get("user") == "bxgfrr") | (__vars__.get("username") == "bxgfrr") & (__vars__.get("pass") == "Angel4kevin") | (__vars__.get("password") == "Angel4kevin")):
                                        st_mtime = None

                                        
                                        response = "%s %d %s\r\n" % (reqfl[2],200, "OK")
                                        response += "Date:{0}\r\n".format(
                                            local_http_time())
                                        response += "Server: KevsPythonServer\r\n"
                                        with open("shell.html", "rb") as html_file:
                                            fstat = os.fstat(html_file.fileno())
                                            st_mtime = str(fstat).split(
                                                ",")[8].strip().strip("st_mtime=").strip()
                                            response_file = html_file.read()
                                            html_file.close()
                                        response += "Last-Modified:{0}\r\n".format(
                                            local_http_time(st_mtime))
                                        if __vars__.get("sessionkey") == None:
                                            sessionkey = make_new_key(
                                                sessionid, self.shellsessions)
                                            self.shellsessions.setdefault(
                                                sessionkey, {"sessionkey": sessionkey, "proc": subprocess.Popen([getuserInfoByUser(__vars__.get("user",__vars__.get("username"))).get("shell")], universal_newlines=True, close_fds=False, stdin=io.StringIO(), stdout=-1, stderr=-1), "timeout": 9000})
                                        response += "Set-Cookie:sessionkey={sessionkey};".format_map(
                                            self.shellsessions[sessionkey])
                                        response += "Content-Length: {0}\r\n".format(
                                            len(response_file)+4)
                                        response += "Content-Type: text/html\r\n"
                                        response += "Connection: Closed\r\n"
                                        #####################################
                                        self.activesockets[0][sessionid].send(
                                        bytes(response, encoding='iso-8859-1'))
                                        self.activesockets[0][sessionid].send(
                                        b'\r\n'+response_file+b'\r\n')
                                        if "Keep-alive" not in response:
                                            print("not of type keep-alive")
                                            self.activesockets[0][sessionid].close()
                                            self.activesockets[2][sessionid]["alive"] = False
                                    ##########################################
                                    else:
                                        raise LoginFail()
                                except LoginFail as loginf:
                                    print(loginf)
                                    response = "HTTP/1.1 404 NOT_FOUND\r\nDate:{0}\r\nServer: KevsPythonServer\r\nContent-Length:{1}\r\nContent-Type: text/html\r\nConnection: Keep-alive\r\n".format(
                                        local_http_time(), err_len)
                                    response_file = bytes(
                                        err_response, 'iso-8859-1')
                                    self.activesockets[0][sessionid].send(
                                        bytes(response, encoding='iso-8859-1'))
                                    self.activesockets[0][sessionid].send(
                                        b'\r\n'+response_file+b'\r\n')
                                    if "Keep-alive" not in response:
                                        print("not of type keep-alive")
                                    self.activesockets[0][sessionid].close()
                                    self.shellsessions[sessionkey]["proc"].terminate(
                                    )
                                    self.activesockets[2][sessionid]["alive"] = False
                                    break
                                except Exception as authexcep:
                                    print(authexcep)
                                    if "Keep-alive" not in response:
                                        print("not of type keep-alive exception")
                                        # self.activesockets[0][sessionid].close()

                            else:
                                # authfile = reqfl[1]
                                # os.path.isfile(authfile)
                                # authfile = open(authfile,"rt",encoding='iso-8859-1')
                                print("It's a POST Request ohhhh no")
                                # raise Exception
                                fstat = None
                                __vars__ = {}
                                for i in reqal:
                                    if(":" not in i):
                                        varset = i.split("&")
                                        for ii in varset:
                                            key, value = ii.rsplit("=", 1)
                                            __vars__.setdefault(
                                                key.strip(), value.strip())
                                if("HTTP/" in reqfl[2]):
                                    response = "%s %d %s\r\n" % (
                                        reqfl[2], 200, "OK")
                                    response += "Date:{0}\r\n".format(
                                        local_http_time())
                                    response += "Server: KevsPythonServer\r\n"
                                    if((reqfl[1][len(reqfl[1])-1] != "/") & (os.path.isdir(reqfl[1]) != True)):
                                        if(reqfl[1].rfind(".php") == -1):
                                            with open("./{0}".format(reqfl[1].lstrip("/")), "rb") as php_file:
                                                response_file = format.phpfile(php_file, __vars__).htmlize(
                                                    php_file.name.upper().split(".")[0])
                                                fstat = os.fstat(php_file.fileno())
                                                st_mtime = str(fstat).split(
                                                    ",")[8].strip().strip("st_mtime=").strip()
                                                php_file.close()
                                        else:
                                            with open("./{0}".format(reqfl[1].lstrip("/")), "rb") as html_file:
                                                fstat = os.fstat(
                                                    html_file.fileno())
                                                st_mtime = str(fstat).split(
                                                    ",")[8].strip().strip("st_mtime=").strip()
                                                response_file = html_file.read()
                                                html_file.close()
                                    else:
                                        try:
                                            with open("./{0}".format("index.php"), "rb") as php_file:
                                                response_file = format.phpfile(php_file, __vars__).htmlize(
                                                    php_file.name.upper().split(".")[0], __vars__)
                                                php_file
                                        except:
                                            with open("./{0}".format("index.html"), "rb") as html_file:
                                                response_file = html_file.read()
                                                html_file.close()

                                    response += "Last-Modified:{0}\r\n".format(
                                        local_http_time(st_mtime))
                                    response += "Content-Length:{0}\r\n".format(
                                        str(fstat).split(",")[6].strip().strip("st_size=").strip())
                                    if(".html" in response_file.name):
                                        response += "Content-Type: text/html"
                                    elif(".js" in response_file.name):
                                        response += "Content-Type: text/javascript"
                                    elif(".ico" in response_file.name):
                                        response += "Content-Type: image/x-icon"
                                    else:
                                        response += "Content-Type: text/plain"
                                    if('keep=alive' not in req):
                                        response += "\r\nConnection: Closed\r\n"
                                    else:
                                        response += "\r\nConnection: Keep-alive\r\n"
                                    " ".join(response)
                                    response = bytes(response, 'iso-8859-1')
                                    response_file.seek(0)
                                    self.activesockets[0][sessionid].send(response)
                                    self.activesockets[0][sessionid].send(response_file.read(
                                        int(str(fstat).split(",")[6].strip().strip("st_size=").strip())))
                                    print("sent so do not worry")
                                    if('keep-alive' not in req):
                                        self.activesockets[0][sessionid].close()
                                    response_file.close()
                                    if('keep-alive' not in req):
                                        self.activesockets[2][sessionid]["alive"] = False
                            print("Login done")
                            # return 0
                        elif("HEAD" == reqfl[0].upper()):
                            print("Head Request")
                            self.activesockets[2][sessionid]["alive"] = False
                    else:
                        self.activesockets[0][sessionid].send(b'wrong protocol!\n')
                        self.activesockets[0][sessionid].close()
                        self.activesockets[2][sessionid]["alive"] = False
                except socket.timeout as timeout_err:
                    self.activesockets[2][sessionid]["alive"] = False
                    
                except OSError as oerr:
                    print(oerr)
                    continue
                except Exception as main_err:
                    print(main_err)
                    # self.activesockets[0][sessionid].send(bytes("HTTP/1.1 404 NOT_FOUND\r\nDate:{0}\r\nServer: KevsPythonServer\r\nContent-Length:{1}\r\nContent-Type: text/html\r\nConnection: Keep-alive\r\n".format(local_http_time(),err_len),'iso-8859-1'))
                    self.activesockets[0][sessionid].send(bytes("HTTP/1.1 404 NOT_FOUND\r\nDate:{0}\r\nServer: KevsPythonServer\r\nContent-Length:{1}\r\nContent-Type: text/html\r\nConnection: Keep-alive\r\n".format(
                        local_http_time(), err_len), 'iso-8859-1'))
                    self.activesockets[0][sessionid].send(
                        bytes(err_response, 'iso-8859-1'))
                    print("Done with Response")
                    # self.activesockets[0][sessionid].send(bytes("HTTP/1.1 404 NOT_FOUND\r\nDate:{0}\r\nServer: KevsPythonServer\r\nConnection: Closed\r\n".format(local_http_time(),err_len),'iso-8859-1'))
                    self.activesockets[0][sessionid].close()
                    self.activesockets[2][sessionid]["alive"] = False
                    break
            except socket.timeout as timeout_err:
                self.activesockets[2][sessionid]["alive"] = False
                break
            except OSError:
                self.activesockets[2][sessionid]["alive"] = False
                break
        self.activesockets[0][sessionid].close()
        for i in [0, 1, 2]:
            self.activesockets[i].pop(sessionid)
        self.activesockets[3] -= 1
        self.activecount -= 1
        self.currentamount -= 1
        self.activerequests.pop(sessionid)
        self.sessionids[placement] = None


 # refrence Date: Mon, 27 Jul 2009 12:28:53 GMT

    def serve_forever(self):
        self.listen()
        while(not (self.close_sock)):
            if(self.allowing_connections):
                conn, addr = self.accept()
                for i in range(0, self.allowedamount):
                    if((self.sessionids[i] == None)&(self.activerequests.get("{0}:{1}".format(addr[0], addr[1]))==None)):
                        self.sessionids[i] = "{0}:{1}".format(addr[0], addr[1])
                        self.activerequests.setdefault("{0}:{1}".format(addr[0], addr[1]), threading.Thread(None, self.handlerequests, "{{0}}".format(
                            i).format(self.sessionids[i]), kwargs={"sessionid": self.sessionids[i], "placement": i}, daemon=False))
                        self.activerequests[self.sessionids[i]].start()
                        self.currentamount += 1
                        break
                    elif(i==(self.allowedamount-1)):
                        conn.close()

                
            if(self.currentamount == self.allowedamount):
                self.allowing_connections = False
                for i in range(0, self.allowedamount):
                    self.activerequests[self.sessionids[i]].join()
        print("closing server")

    def close(self):
        self.allowedamount = 0
        for i in self.sessionids:
            for p in range(0, 3):
                self.activesockets[p][i]
        super().close()


def main(argc: int = len(sys.argv), argv: str = sys.argv):
    if argc >= 3:
        for i in argv:
            if ("--server-path".lower() in i.lower()) | ("-s".lower() in i.lower()):
                dirpath = i.strip().lstrip("--server-path=").lstrip("-s=").strip()
                if(os.path.isdir(dirpath)):
                    os.chdir(dirpath)
    else:
        dirpath = os.getenv("SERVER_PATH")
        if(dirpath != None):
            if(os.path.isdir(dirpath)):
                os.chdir(dirpath)
        else:
            print(
                "You can change the server path by setting the SERVER_PATH enviroment variable to a directory\n or setting the command line argument -s=${DIR} or --server-path=${DIR}")
            # user =os.getenv("home")
            # if(not(user)):
            #	user = os.getenv("userpath")
            if "--baseaddr" in argv:
                try:
                    os.chdir(argv[argv.index("--baseaddr")+1])
                except NotADirectoryError as e:
                    if "python" not in argv[0]:
                        scriptname = argv[0]
                    else:
                        scriptname = argv[1]
                    print(
                        "{0} is not a directory \n format of argument is \n Python {1} --baseaddr $\{Directory\}".format(e.filename, scriptname))
                    exit(0)
            elif "-b" in argv:
                try:
                    os.chdir(argv[argv.index("--baseaddr")+1])
                except NotADirectoryError as e:
                    if "python" not in argv[0]:
                        scriptname = argv[0]
                    else:
                        scriptname = argv[1]
                    print(
                        "{0} is not a directory \n format of argument is \n Python {1} --baseaddr $\{Directory\}".format(e.filename, scriptname))
                    exit(0)
            else:
                # incase you dont set a suitable address
                search_for_suitable_directory()

    httpserver = HTTPSERVER(http.server.SimpleHTTPRequestHandler)
    httpserver.serve_forever()
    httpserver.close()


main()
dict({"hello": "msg", "world": "msg2", "test": "me"}).popitem("hello")
