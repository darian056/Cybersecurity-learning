import recursive_monitor
import os
import hashlib
from pathlib import Path
import time
from colorama import Fore, Back, Style, init





def Calculate_File_hash(path):
    with open(path, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")

    file_hash = digest.hexdigest()
    f_path_hash = str(Path(path).resolve()) + " | " + file_hash + "\n"

    return f_path_hash

import time
from pathlib import Path

def Logs(path, event, old_hash=None):
    log_dir = Path("fim_Logs")
    log_dir.mkdir(exist_ok=True)
    l_path = log_dir / "Logs.txt"
    
    full_date_and_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if event == "DELETED":
        log_data = f"{full_date_and_time} | {event} | {Path(path).resolve()} | {old_hash}"
    else:
        path_hash = Calculate_File_hash(path)
        log_data = f"{full_date_and_time} | {event} | {path_hash}"

    with open(l_path, "a") as file:
        log = file.write(log_data)
        
    return log

def option_a(b_path):
        if b_path.exists():
            b_path.unlink()

        p = Path.cwd()
        data_dir = p / "fim_data"
        log_dir = p / "fim_Logs"

        with open(b_path, "a") as basefile:
            for f in p.rglob("*"):

                if f.is_relative_to(data_dir):
                    continue
                elif f.is_relative_to(log_dir):
                    continue
                else:
                    if f.is_file():
                        basefile.write(Calculate_File_hash(f))




def option_b(b_path):
    fileHashDict = {}
    p = Path.cwd()
    logs_dir = p / "fim_Logs"   
    data_dir = p / "fim_data"

    
    with open(b_path, "r") as file:
        for f in p.rglob("*"):
            if f.is_relative_to(data_dir):
                continue
            elif f.is_relative_to(logs_dir):
                continue
            else:
                for line in file:
                    parts = line.strip().split(" | ")
                    if len(parts) == 2:
                        fileHashDict[str(Path(parts[0]).resolve())] = parts[1]

    return fileHashDict


if __name__ == "__main__":

    print("What would you like to do?")
    print("A) Collect new Baseline? \nB) Begin monitoring files with saved Baseline")

    userin = input("Please enter A or B: ")

    # Setup the data directory and baseline path using Pathlib
    data_dir = Path("fim_data")
    data_dir.mkdir(exist_ok=True)
    b_path = data_dir / "baseline.txt"

    recursive_monitor.scanner(b_path,userin)
            
        




