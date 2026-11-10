import baselineengine
import os
import hashlib
from pathlib import Path
import time
from colorama import Fore, Back, Style, init



def scanner(b_path, userin):

    root = Path.cwd()
    logP = root / "fim_Logs"
    DataDir = root / "fim_data"


    if userin.casefold() == "a":
        baselineengine.option_a(b_path) #calling A

    elif userin.casefold() == "b":
        fileHashDict = baselineengine.option_b(b_path) # calling B

        while(True):
            time.sleep(1)

            p = Path.cwd() # this is giving me the path for the current folder im in
             # this is listing folders and filenames
            
            for f in p.rglob("*"):


                
                if f.is_relative_to(DataDir):
                    continue
                if f.is_relative_to(logP):
                    continue
                if not f.is_file():
                    continue


                file_path_str = str(Path(f).resolve())
                path_hash = baselineengine.Calculate_File_hash(str(f)) # sending the file to be hashed 

                parts = path_hash.split("|")  # after returning it I split it

                current_hash = parts[1].strip()
                
                if file_path_str not in fileHashDict:
                    print(Fore.BLUE + "New file created: ", file_path_str)
                    fileHashDict[file_path_str] = current_hash
                    baselineengine.Logs(file_path_str, "FILE CREATED")
                    
                else:
                    oldHash = fileHashDict[file_path_str]

                    if current_hash != oldHash:
                        print(Fore.RED + "file has been changed: ", file_path_str)
                        baselineengine.Logs(str(f), "MODIFIED")
                        new_hash = baselineengine.Calculate_File_hash(str(f))
                        
                        with open(b_path, "r") as file:
                            lines = file.readlines()

                        with open(b_path, "w") as file:
                            for line in lines:
                                if oldHash in line:
                                    file.write(new_hash)
                                else:
                                    file.write(line)
                                    
                        fileHashDict[file_path_str] = current_hash
                        
                    else:
                        pass
                        
            tracked_files = list(fileHashDict.keys())
            for tracked in tracked_files:
                if not os.path.exists(tracked):
                    print(Fore.RED+"File deleted: ", tracked)

                    baselineengine.Logs(tracked, "DELETED", fileHashDict[tracked])

                    del fileHashDict[tracked]

                    with open(b_path, "r") as file:
                        line = file.readlines()

                    with open(b_path, "w") as file:
                        for lines in line:
                            if tracked not in lines:
                                file.writelines(lines)
