#! python3
import os
tgtdir=r'E:\yamaPythonScripts'
for curDir, dirs, files in os.walk(tgtdir): 
    for file in files:    
        if file[-4:]=='.bat':   
            print(os.path.join(curDir,file))
print('Done---------------')       