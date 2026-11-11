import recursive_monitor
import sys
import hashlib
from pathlib import Path
import time
from colorama import Fore, Back, Style, init
import logging





def Calculate_File_hash(path):
    with open(path, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")

    file_hash = digest.hexdigest()
    f_path_hash = str(Path(path).resolve()) + " | " + file_hash + "\n"

    return f_path_hash

import time
from pathlib import Path

def Logs(path, event=None):
    log_dir = Path("fim_Logs")
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
    filename=log_dir / 'dev.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s %(process)d %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True)

    resolved_path = Path(path).resolve()

    if event == "DELETED":
        message = f"{event} | {resolved_path}"
    else:
        message = f"{event} | {resolved_path}" 

    logging.info(message)

def option_a(b_path):

        b_path.parent.mkdir(exist_ok=True)

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
        for line in file:
            parts = line.strip().split(" | ")
            if len(parts) == 2:
                fileHashDict[str(Path(parts[0]).resolve())] = parts[1]

    recursive_monitor.start_fim_daemon()


if __name__ == "__main__":

    print("What would you like to do?")
    print("A) Collect new Baseline? \nB) Begin monitoring files with saved Baseline")

    userin = input("Please enter A or B: ")

    path = Path.cwd()
    b_path = path / "fim_data" / "baseline.txt"



    if userin == "A":
        option_a(b_path)
    elif userin == "B":
        option_b(b_path)

        



