#! /usr/bin/python3

import sys
import os
#./run.py ./cr-1/ rm
workdir=sys.argv[1]
bcname=sys.argv[2]


def main():
    wrapper_target_functions(workdir,bcname)

def wrapper_target_functions(workDir,bcName):
    bcname=bcName
    workdir=workDir
    bcfile=workdir+bcname+'.bc'
    target_functions_file=workdir+bcname+'_target_functions'
    print("debug",target_functions_file)
    with open(target_functions_file, 'r') as target_functions:
        for target in target_functions.readlines():
            print("debug:target=",target)
            target=target.strip()
            target_name='macke_'+target+'_main'
            outbcfile=workdir+bcname+'-macke-'+target+'-main.bc'
            outusebcfile=workdir+bcname+'-use-'+target+'-main.bc'
            if(target=="main"):
                cmd1='cp '+bcfile+' '+outbcfile
                cmd3='cp '+outbcfile+' '+outusebcfile
            else:
                cmd1='opt -load ~/deploy/macke-opt-llvm/bin/libMackeOpt.so -encapsulatesymbolic '+bcfile+' -encapsulatedfunction '+target+' -o '+outbcfile
                cmd3='opt -load ~/deploy/macke-opt-llvm/bin/libMackeOpt.so -changeentrypoint '+ outbcfile +' -newentryfunction '+ target_name+' -o '+ outusebcfile
            print("debug: cmd1=",cmd1)
            print("debug: cmd3=",cmd3)
            os.system(cmd1)
            os.system(cmd3)

if __name__ == "__main__":
    main()

