import argparse
import string
import os
from qlbuild import config

# Quarter-Build: QC Model Compiler v0.131230
# By Wade Harkins <vdtdev@gmail.com>
# ------------------------------------------
# Command line arguments:
# -qc <filename>
#	filename = qc filename
# -ini <filename>
#	filename = path to quarte-build ini file

def __startup__():
	""" Primary method for QC Builder """
	print("Q-L QC Builder")
	cmd = argparse.ArgumentParser("Build model files from Valve QC Scripts",
								  usage="qlqc -qc [QCFileName]")
	cmd.add_argument("-qc", dest="QCFileName", help="QC script file",
					default="NAN")
	cmd.add_argument("-ini",dest="INIPath",help="QB configuration ini path",
					default="qlbs.ini")
	#cmd.print_help()

	z = cmd.parse_args()
	d=vars(z)
	# load tool path
	cfg = config(d["INIPath"])
	tool_path = cfg.setting("toolsrc")
	if d.has_key("QCFileName"):
		if d["QCFileName"] != "NAN":
			os.execl(tool_path+"\\run_studiomdl.bat",d["QCFileName"])
		else:
			cmd.print_help()
				 
if __name__=="__main__":
	__startup__()
