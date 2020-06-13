# Executes shell commands in file supplied as argument
# e.g: python exec.py golicmds.txt

import sys
import os
filename=sys.argv[1]

with open(filename) as fp:
  for line in fp:
    s=line.rstrip().lstrip()
    print("Executing [%s]..." % s)
    os.system(s) 
