from io import FileIO, StringIO
import os
import time
import sqlite3
import gzip
import io
import subprocess


class phpfile():
    file = ""

    def __init__(self, php_file: str, __vars__: dict):
        pre_code = ""
        end_code = ""
        for i in __vars__:
            if(__vars__[i].__class__.lstrip("<class").rstrip(">").strip().strip("\"").strip("\'").strip("\"") == str):
                pre_code += "$_POST[\"{key}\"]=\"{value}\";".format(
                    kwargs={"key": i, "value": __vars__[i]})
            else:
                pre_code += "$_POST[\"{key}\"]={value};".format(
                    kwargs={"key": i, "value": __vars__[i]})
        pre_code += php_file
        self.file = subprocess.Popen(
            ["/home/kevin/assignmentserver/php-cli/usr/bin/php7.2", "-B", "\"{precode}\"".format()], stdin=StringIO(pre_code), stdout=-1, stderr=-1, close_fds=False)
        exitcode = self.file.wait()
        if(exitcode == 0):
            proc = self.file
            self.file = self.file.stdout.read()
            proc.terminate()

    def htmlize(self, title, args: dict = None):
        prepend = b''
        append = b''
        for i in [b'<!doctype html>', b'<html>', b'<head>', b'<title>', b'</title>', b'<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">', b'</head>', b'<body>']:
            if(i not in self.file.lower()):
                if i != b'<title>':
                    prepend += i
                else:
                    prepend += i+title
        self.file = bytes(prepend + self.file)
        for i in [b'</body>', b'</html>']:
            if(i not in self.file.lower()):
                append += i
        self.file = bytes(self.file+append)
        return self.file
