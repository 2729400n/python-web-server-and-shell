#!/usr/bin/env python3
import struct,os
def readrecord(record:bytes):
	record_type = record[0]
	ssl_tls_version = record[1:3]
	if(record_type==b'\x16'):
		readHelloRequest(record,ssl_tls_version)
	elif(record_type==b'\x14'):
		readHelloRequest(record,ssl_tls_version)
	elif(record_type==b'\x15'):
		readHelloRequest(record,ssl_tls_version)
	elif(record_type==b'\x17'):
		readHelloRequest(record,ssl_tls_version)
	else:
		pass

def readHelloRequest(record:bytes,version:bytes):
	pass