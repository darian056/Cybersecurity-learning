import baselineengine
import os
from pathlib import Path
import time
from colorama import Fore, Back, Style, init
import sys
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer




class MyEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        p = Path.cwd()
        self.logs_dir = (p / "fim_Logs").resolve()
        self.data_dir = (p / "fim_data").resolve()       

    def should_ignore(self, p):
        resolved_path = Path(p).resolve()

        if resolved_path.is_relative_to(self.data_dir) or resolved_path.is_relative_to(self.logs_dir):
            return True
        return False

    def on_modified(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
        print(f"File modified: {event.src_path}")
        baselineengine.Logs(event.src_path)
        

    def on_created(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
        print(f"File created: {event.src_path}")
        baselineengine.Logs(event.src_path)

    def on_deleted(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
        print(f"File deleted: {event.src_path}")
        baselineengine.Logs(event.src_path, "DELETED")

        



def start_fim_daemon():
    try:
        event_handler = MyEventHandler()
        w_path = Path.cwd()
        observer = Observer()
        observer.schedule(event_handler, path=str(w_path), recursive=True)
        observer.start()
        while True:



            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping Daemon")
        observer.stop()
    observer.join()




   











