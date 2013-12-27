""" Quarter-Life Build
    v0.2.20120929
    by Wade Harkins <vdtdev@gmail.com>"""

import argparse
import string

# command names from batch version
__commands__ = ["getMaterials","putMaterials","getAssets","putAssets","build_materials"]

cfg = None

def __startup__():
    parser = argparse.ArgumentParser(description='Quarter-Life Build System (QLBS) v0.2')
    parser.add_argument('tool',default='noargs',
                        help='name of tool to invoke',action='store')
    parser.add_argument('args',nargs='*',help='tool arguments',action='store')
    args = parser.parse_args('tool','args')
    arg=vars(args)
    run_tool(arg)

def run_tool(arg):
    cfg=config('qlbs.ini')
    if arg.has_key("tool"):
        if arg['tool']=='build_materials':
            build_materials(arg['tool_args'])
    else:
        parser.print_help()

""" Read a dictionary of settings from a file on disk """
class config:
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
    """ Read a setting from the loaded configuration file """
    def setting(self,prop):
        return self.__props__[prop]

""" implements the functionality of build_materials.bat """
def build_materials(path):
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

if __name__=="__main__":
    print("[QLBS]")
    __startup__()
