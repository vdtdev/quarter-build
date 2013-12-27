""" Quarter-Life Build
	v0.2.20120929
	by Wade Harkins <vdtdev@gmail.com>"""

import argparse
import string

# command names from batch version
__commands__ = ["getMaterials","putMaterials","getAssets","putAssets","build_materials"]
__parser__ = None
cfg = None

def __startup__():
	parser = argparse.ArgumentParser(description='Quarter-Life Build System (QLBS) v0.2')
	parser.add_argument('tool',default='noargs',
						help='name of tool to invoke',action='store')
	parser.add_argument('args',nargs='*',help='tool arguments',action='store')
	args = parser.parse_args(['tool','args'])
	
	arg=vars(args)
	if arg.has_key("tool"):
		if not arg['tool'] in __commands__:
			parser.print_help()
			exit(0)
	run_tool(arg)

def run_tool(arg,args):
	""" Execute tool indicated in the commandline, or show help """
	cfg=config('qlbs.ini')
	if arg['tool']=='build_materials':
		build_materials(arg['tool_args'])
		exit(0)
	if arg['tool']=="getAssets" or arg['tool']=="putAssets":
		tool = asset_management(cfg,arg['tool'])
		exit(0);

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


def build_materials(path):
	""" implements the functionality of build_materials.bat """
	mat_src = cfg.setting('matsrc')
	dst_root = cfg.setting('matdst')
	if dst_root[len(dst_root)-1]!='\\':
		dst_root = string.join([dst_root, path],'\\')
	if mat_src[len(mat_src)-1]!='\\':
		mat_src = string.join([mat_src, path],'\\')
	dst2 = dst_root + path
	src2 = mat_src + path
	os.system('mkdir ' + dst2)
	os.system('mkdir ' + src2)
	shutil.copy(mat_src + '*.vmt',dst_root)
	shutil.copy(src2 + '\\*.vmt',dst2)
	shutil.copy(src2 + '\\*.vmt',dst2)
	print('Finished executing')	


class asset_management:
	""" Asset management functionality (get/put/backup, etc) """
	def __init__(self,config,command):
		if command in __commands__:
			self._mode_=command
		err=0;
		if not config.setting('scrsrc')==None:
			print "Asset source path not defined. (Expected value for scrsrc in qlbs.ini)"
			err+=1
		if not config.setting('scrbackup')==None:
			print "Asset backup path not defined. (Expected value for scrbackup in qlbs.ini"
			err+=10
		if err!=0:
			print "Terminating."
			exit(err)
			
	
if __name__=="__main__":
	print("[QLBS]")
	__startup__()
