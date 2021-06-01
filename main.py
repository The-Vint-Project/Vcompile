import os, sys
from read import VINTFile

abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

file=VINTFile("test.vmf")
file.parse()