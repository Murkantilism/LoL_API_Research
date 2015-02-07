__author__ = 'Deniz'

import os.path
import shutil

def main():
    source0 = os.curdir + "\_outControl_0to15\\"
    source1 = os.curdir + "\_outControl_16to30\\"
    dest = os.curdir + "\_outControl\\"

    sourcefiles = {os.path.splitext(x)[0] for x in os.listdir(source0) if os.path.splitext(x)[1] == '.txt'}
    source1files = {os.path.splitext(x)[0] for x in os.listdir(source1) if os.path.splitext(x)[1] == '.txt'}

    for missing in sourcefiles - source1files:   # calculate the difference
        source0file = os.path.join(source0, missing + '.txt')
        source1file = os.path.join(source1, missing + '.txt')
        shutil.copy(source0file, dest)

    #deleteMissingFiles(source0, dest)
    #deleteMissingFiles(source1, dest)

def deleteMissingFiles(source, dest):
    filesToDelete = {os.path.splitext(x)[0] for x in os.listdir(dest) if os.path.splitext(x)[1] == '.txt'}
    for file in filesToDelete:
        #print file
        if os.path.exists(os.curdir+"\_outControl_0to15\\"+file+".txt"):
            os.remove(os.curdir+"\_outControl_0to15\\"+file+".txt")
        if os.path.exists(os.curdir+"\_outControl_16to30\\"+file+".txt"):
            os.remove(os.curdir+"\_outControl_16to30\\"+file+".txt")

if __name__ == "__main__":
    main()