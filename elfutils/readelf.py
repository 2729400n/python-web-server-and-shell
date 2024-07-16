import os,io,builtins,struct

def readproghdr(offset,file:io.BufferedRandom,bit_encoding=64,data_encoding=1):
	file.seek(offset)
	if(bit_encoding==64):
		fmt = "@Q"
	else:
		fmt = "@I"
	p_type = file.read(4)
	if(bit_encoding==64):
		p_flags = struct.unpack("@I",file.read(4))
	p_offset = struct.unpack(fmt,file.read(bit_encoding/8))
	p_vaddr = struct.unpack(fmt,file.read(bit_encoding/8))
	p_filesz = struct.unpack(fmt,file.read(bit_encoding/8))
	p_memsz = struct.unpack(fmt,file.read(bit_encoding/8))
	if(bit_encoding!=64):
		p_flags = struct.unpack("@I",file.read(4))
	p_align = struct.unpack(fmt,file.read(bit_encoding/8))


def readelf(path="./a.out"):
	file = open(path,"wb+",closefd=False)
	file.seek(0)
	header = file.read(4)
	if(header!="\x00ELF"):
		return -1
	file.seek(4)
	bitencoding = file.read(1)
	dataencoding = file.read(1)
	bit_encoding=struct.unpack("@b",bitencoding)[0]*32
	data_encoding = struct.unpack("@b",dataencoding)
	elf_version = struct.unpack("@b",file.read(1))
	osabi = struct.unpack("@b",file.read(1))
	abi_version = struct.unpack("@b",file.read(1))
	padding = file.read(8)
	cputype = struct.unpack("@h",file.read(2))
	machine_type = struct.unpack("@h",file.read(2))
	version_type = struct.unpack("@I",file.read(4))
	if(bit_encoding==64):
		fmt = "@Q"
	else:
		fmt = "@I"
		
	_entry_offset = struct.unpack(fmt,file.read(bit_encoding/8))
	_progheader_offset = struct.unpack(fmt,file.read(bit_encoding/8))
	_secheader_offest = struct.unpack(fmt,file.read(bit_encoding/8))
	_flags = struct.unpack("@I",file.read(4))
	_elfheader_size = struct.unpack("@H",file.read(2))
	_progheaderesize = struct.unpack("@H",file.read(2))
	_progheader_num = struct.unpack("@H",file.read(2))
	_secheadere_size = struct.unpack("@H",file.read(2))
	_secheadere_num = struct.unpack("@H",file.read(2))
	_strsecindex = struct.unpack("@H",file.read(2))
	phdr = readproghdr(_progheader_offset,file,bit_encoding,data_encoding)
