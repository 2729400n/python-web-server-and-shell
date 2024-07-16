from io import FileIO
import os,time,sqlite3,gzip,io,subprocess
class phpfile():
	file=""
	def __init__(self,php_file: str,__vars__:dict):
		pre_code ="<?"
		for i in __vars__:
			pre_code+="$_POST[{key}]={value};\n".format_map({"key":i,"value":__vars__[i]})
		pre_code+="?>"
		proc = subprocess.Popen(["/home/kevin/assignmentserver/php-cli/usr/bin/php7.2"],stdin=io.StringIO(),close_fds=False)
		proc.stdin.write(pre_code + php_file)
		proc.stdin.flush()
		exitcode = proc.wait()
		if(exitcode==0):
			self.file=proc.stdout.read()
		proc.terminate()
		return self
		
			
	def htmlize(self,title,args:dict=None):
		prepend =b''
		append =b''
		for i in [b'<!doctype html>',b'<html>',b'<head>',b'<title>',b'</title>',b'<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">',b'</head>',b'<body>']:
			if(i not in self.file.lower()):
				if i !=b'<title>':
					prepend+=i
				else:
					prepend+=i+title
		self.file=bytes(prepend + self.file)
		for i in [b'</body>',b'</html>']:
			if(i not in self.file.lower()):
				append+=i
		self.file=bytes(self.file+append)
		return self.file

		

