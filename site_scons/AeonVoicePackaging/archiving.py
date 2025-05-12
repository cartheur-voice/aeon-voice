# -*- coding: utf-8; mode: Python; indent-tabs-mode: t -*-

import os.path
import zipfile
from SCons.Script import Value
from .common import *

def archive(target,source,env):
	with zipfile.ZipFile(str(target[0]),"w",zipfile.ZIP_DEFLATED) as f:
		for i in range(0, len(source), 3):
			infile=source[i]
			outpath=source[i+1].read()
			on_disk=source[i+2].read()
			if on_disk:
				f.write(str(infile), outpath)
			else:
				f.writestr(outpath, infile.read())

class archiver(packager):
	def __init__(self,name,outdir,env,ext="zip"):
		super(archiver,self).__init__(name,outdir,env,ext)

	def package(self):
		sources=list()
		for f in self.files:
			sources.append(f.infile)
			sources.append(Value(f.outpath))
			sources.append(Value(f.on_disk))
		return self.env.Command(self.outfile,sources,archive)[0]
