# -*- coding: utf-8 -*-
import os
import shutil
from itertools import chain
from pathlib import Path
import glob


def mycopyfile(srcfile,dstfile):
    if srcfile.exists() and (not os.path.exists(dstfile)):
        with dstfile.open(mode='xb') as fid: 
            fid.write(srcfile.read_bytes())

data_root: Path  = Path("D:/workspace/python/pypet/data/")    # Replace with yours
out_dir: Path  = Path("D:/workspace/python/pypet/out")
if __name__ == "__main__":
    speaker_dirs = data_root.glob("*.metadata")
    for vodio in speaker_dirs:
        if os.path.exists(vodio):
            filename = os.path.basename(vodio)
            s = filename.split(".")[0]
            speaker = s[0:15]

            out_dir.joinpath(speaker).mkdir(exist_ok=True)
            
            mycopyfile(data_root.joinpath(s + ".lab"),out_dir.joinpath(speaker).joinpath(s + ".lab"))
            mycopyfile(data_root.joinpath(s + ".txt"),out_dir.joinpath(speaker).joinpath(s + ".txt"))
            mycopyfile(data_root.joinpath(s + ".wav"),out_dir.joinpath(speaker).joinpath(s + ".wav"))
            mycopyfile(data_root.joinpath(s + ".metadata"),out_dir.joinpath(speaker).joinpath(s + ".metadata"))
       

    
                    
    