import io
import fileinput
import builtins
import asyncio
import subprocess
import tty
import textwrap
import random
import readline
import sys
import os

g = os.pipe2(os.O_WRONLY)

def check_flags():
	flags = []
	for i in range(0,0xffffffff):
		try:
			os.pipe2(i)
			flags.append(i)
		except:
			pass
	return flags