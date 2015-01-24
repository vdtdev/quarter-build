""" Quarter-Life Build
	v0.2.20150124
	by Wade Harkins <vdtdev@gmail.com>"""
import textwrap
import argparse
import string
import time
import sys
import shutil
import fnmatch
from os import path
import os

# command names from batch version
__commands__=[['get','materials'],['get','assets'],['put','materials'],
				['put','assets'],['build','materials']]
__actions__=['get','put','build']
__targets__=['materials','assets']
__asset_args__=['U','C','N','A']
__parser__ = None
__arguments__=None
__cfg__ = None

def __startup__():
	parser = argparse.ArgumentParser(description='Quarter-Life Build System (QLBS) v0.2',
			epilog=textwrap.dedent('''Valid Tool Arguments:
	U	Copy only updated files
	C	Copy only changed files
	N	Copy only new files
	A	Copy all (default)'''),
			formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('action',metavar='action',choices=__actions__,
						help='Tool action (get, set, build)')
	parser.add_argument('target',metavar='target',choices=__targets__,
						help='Content type to target (assets, materials)')
	parser.add_argument('--args',dest='args',choices=__asset_args__,
						help='Arguments to pass to tool',action='store',required=False)
	parser.add_argument('--path',dest='matpath',help='Material folder to build',
						required=False,default='*nopath*')
	print(parser.description)
	# exit if no arguments were passed, or just one
	if len(sys.argv)==1 or len(sys.argv)==2:
		parser.print_help()
		exit(0)
		
	args = parser.parse_args()
	arg=vars(args)
	run_tool(arg,args)

def run_tool(arg,args):
	""" Execute tool indicated in the commandline, or show help """
	__cfg__=config('qlbs.ini')
	__arguments__=arg
	if arg['target']=='materials':
		# Material actions
		if arg['action']=='build':
			# Build materials
			build_materials(__cfg__,arg['matpath'])
			exit(0)
		if arg['action']=='get':
			# Build materials
			get_materials(__cfg__,arg['matpath'])
			exit(0)
			
	if arg['target']=='assets':
		command = [arg['action'],arg['target']]
		arguments = {
		"action":arg['action'],"target":arg['target'],
		"args":arg["args"]}
		# Asset actions
		if arg['action']=='get':
			tool = asset_management(__cfg__,command,arguments)
			tool.execute
			exit(0)
		if arg['action']=='put':
			tool = asset_management(__cfg__,command,arguments)
			tool.execute()
			exit(0)
		print ("Invalid action provided")
		exit(0)

# INI Config File Parser
class config:
	""" Read a dictionary of settings from a file on disk """
	def __init__(self,cfgfile):
		self.__props__=dict()
		f = open(cfgfile,'r')
		s="0"
		eof=0
		while eof==0:
			s=f.readline()
			if len(s)>0:
				# ignore the input if it is a section or a comment
				if s[0] != '[' and s[0] != ';':
					p=s.split("=")
					self.__props__[p[0].strip()]=p[1].strip()
			else:
				eof=1
		f.close()
	def setting(self,prop):
		""" Read a setting from the loaded configuration file """
		if not self.__props__.has_key(prop):
			return None
		return self.__props__[prop]


def build_materials(cfg,spath):
	""" implements the functionality of build_materials.bat 
		cfg - instance of Config with qlbs.ini loaded
		spath - sub folder of material source folder to copy from
	"""
	mat_src = cfg.setting('matsrc')
	dst_root = cfg.setting('matdst')
	
	# if no subpath is specified, use the root
	if not spath=='*nopath*':
		if dst_root[len(dst_root)-1]!=path.sep:
			dst2 = string.join([dst_root, spath],path.sep)
		else:
			dst2=dst_root + path.sep + spath
		if mat_src[len(mat_src)-1]!=path.sep:
			src2 = string.join([mat_src, spath],path.sep)
		else:
			src2 = mat_src + path.sep + spath
		
	os.system('mkdir ' + dst2)
	os.system('mkdir ' + src2)
	
	src_files = os.listdir(src2)
	
	for fn in src_files:
		if fnmatch.fnmatch(fn,'*.vmt') or fnmatch.fnmatch(fn,'*.vtf'):
			shutil.copy(src2 +path.sep+ fn,dst2)
			print('Copying '+fn+'...')
	
	print('Finished executing')	

def get_materials(cfg,spath):
	""" implements the functionality of build_materials.bat 
		cfg - instance of Config with qlbs.ini loaded
		spath - sub folder of material source folder to copy from
	"""
	mat_src = cfg.setting('matdst')
	dst_root = cfg.setting('matsrc')
	dst = dst_root
	src = mat_src
	
	# if no subpath is specified, use the root
	if not spath=='*nopath*':
		if dst_root[len(dst_root)-1]!=path.sep:
			dst2 = string.join([dst_root, spath],path.sep)
		else:
			dst2=dst_root + path.sep + spath
		if mat_src[len(mat_src)-1]!=path.sep:
			src2 = string.join([mat_src, spath],path.sep)
		else:
			src2 = mat_src + path.sep + spath
		
	os.system('mkdir ' + dst)
	os.system('mkdir ' + src)
	
	src_files = os.listdir(src)
	
	for fn in src_files:
		if fnmatch.fnmatch(fn,'*.vmt') or fnmatch.fnmatch(fn,'*.vtf'):
			shutil.copy(src +path.sep+ fn,dst)
			print('Copying '+fn+'...')
	
	print('Finished executing')	

# Quarter-Build System - Asset Management Class
# v0.131229 by Wade Harkins <vdtdev@gmail.com>
# ---------------------------------------------
# Provides asset management capabilities get and put
class asset_management:
	""" Asset management functionality (get/put/backup, etc) """
	def __init__(self,config,command,args):
		#print(config)
		#print(command)
		#print(__arguments__)
		if command in __commands__:
			self._mode_=command
		self._args_=args
		self._config_=config
		err=0
		if config.setting('scrsrc')==None:
			print "Asset source path not defined. (Expected value for scrsrc in qlbs.ini)"
			err+=1
		if config.setting('scrbackup')==None:
			print "Asset backup path not defined. (Expected value for scrbackup in qlbs.ini"
			err+=10
		if err!=0:
			print "Terminating."
			exit(err)
	
	
	def execute(self):
		""" Execute managment command """
		if self._mode_==['get','assets']:
			self.get_assets
			return 0
		if self._mode_==['put','assets']:
			self.put_assets
			return 0
		print("Invalid action.")
		
	
	def determine_path(self):
		""" Determine the next available parts folder """
		ti = time.localtime
		tentative_name = str(ti.tm_year) + str(ti.tm_mon) + str(ti.tm_mday)
		original_name=tentative_name
		counter=1
		name_decided = False
		while not name_decided and counter < 45:
			name_decided = path.exists(self._config_.setting("scrdst") +
									   path.sep + tentative_name)
			if name_decided:
				tentative_name=original_name + '-' + str(counter)
				counter+=1
		return tentative_name
	
	def working_asset_paths(self):
		""" Dictionary of the working paths for script, config, and resource assets """
		scrsrc = self._config_.setting("scrsrc")
		return {"scr": scrsrc + path.sep + "scripts", "cfg": scrsrc + path.sep + "cfg", "res": scrsrc + path.sep + "resource"}
	
	def get_assets(self):
		""" Copy assets from script, resource, media and cfg from the 
			binary folder to a folder in the local parts folder """
		
		dst_path = self._config_.setting("scrsrc")
	
		scr_files = os.listdir(self._config_.setting("buildroot") + path.sep + "scripts")
		cfg_files = os.listdir(self._config_.setting("buildroot") + path.sep + "cfg")
		res_files = os.listdir(self._config_.setting("buildroot") + path.sep + "resource")
		
		scr_dst = self.working_asset_paths()["scr"]
		cfg_dst = self.working_asset_paths()["cfg"]
		res_dst = self.working_asset_paths()["res"]
		
		
		os.system('mkdir ' + scr_dst)
		os.system('mkdir ' + cfg_dst)
		os.system('mkdir ' + res_dst)
		
		print("Coping assets... " + scr_dst)
	
		for fn in scr_files:
			shutil.copy(scr_files + path.sep + fn,scr_dst)
			print("Copying script "+ fn +"...")
		print("Coping assets... " + cfg_dst)
		for fn in cfg_files:
			shutil.copy(cfg_files + path.sep + fn,cfg_dst)
			print("Copying script "+fn+"...")
		print("Coping assets... " + res_dst)
		for fn in res_files:
			shutil.copy(res_files + path.sep + fn,res_dst)
			print("Copying script " + fn + "...")

if __name__=="__main__":
	print("[QLBS]")
	__startup__()
