import argparse
import string
import os

def __startup__():
    print("Q-L QC Builder")
    cmd = argparse.ArgumentParser("Build model files from Valve QC Scripts",usage="qlqc -qc [QCFileName]")
    cmd.add_argument("-qc", dest="QCFileName", help="QC script file",default="NAN")
    cmd.print_help()

    z = cmd.parse_args()
    d=vars(z)
    if d.has_key("QCFileName"):
        if d["QCFileName"] != "NAN":
            os.execl("f:\dev\quarterlife\run_studiomdl.bat",d["QCFileName"])
    else:
        cmd.print_help()
                 
if __name__=="__main__":
    __startup__()
