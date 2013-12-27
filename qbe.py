"""
    Quarter-Life SOURCE engine build utilities
    v0.2 - port from windows batch to python
    by Wade Harkins <vdtdev@gmail.com>
    """

import argparse

# command names from batch version
__commands__ = ["getMaterials","putMaterials","getAssets","putAssets","build_materials"]

class config:
    def __init__(self,cfgfile):
        self.__props__=dict()
        f = open(cfgfile,'r')
        s="0"
        while s != "":
            s=f.readline()
            p=string.split(s,"=")
            self.__props__[p[1]]=p[0]
        f.close()

    def setting(self,prop):
        return self.__props__[prop]


class build_materials:
    def __init__(self,cfgpath):
        self.__banner__="Build-Materials v0.2"
        self.__usage__="Usage: build-materials [root path]"
        self.__config__=config(cfgpath)
        
