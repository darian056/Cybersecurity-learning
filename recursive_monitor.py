import baselineengine
from pathlib import Path
import time
from colorama import Fore, Back, Style, init
from watchdog.events import FileSystemEvent, FileSystemEventHandler, LoggingEventHandler
from watchdog.observers import Observer
from rich.console import Console




class MyEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        p = Path.cwd()
        self.logs_dir = (p / "fim_Logs").resolve()
        self.data_dir = (p / "fim_data").resolve() 
        self.last_events = {}    


    
    def should_ignore(self, p):
        resolved_path = Path(p).resolve()

        if resolved_path.is_relative_to(self.data_dir) or resolved_path.is_relative_to(self.logs_dir):
            return True
        return False

    def is_debounce(self, p):
        current_time = time.time()
        resolved_path = Path(p).resolve()

        if resolved_path in self.last_events:
            if current_time - self.last_events[resolved_path] < 1.5:
                return True
        self.last_events[resolved_path] = current_time
        print(self.last_events)
        return False


    def on_modified(self, event):
        if event.is_directory or self.should_ignore(event.src_path) or self.is_debounce(event.src_path):
            return
        print(Fore.BLUE+f"File modified: {event.src_path}")
        baselineengine.Logs(event.src_path, "MODIFIED")
        

    def on_created(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
        print(Fore.GREEN+f"File created: {event.src_path}")
        baselineengine.Logs(event.src_path, "CREATED")

    def on_deleted(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
        print(Fore.RED+f"File deleted: {event.src_path}")
        baselineengine.Logs(event.src_path, "DELETED")




        
console = Console() #simple CLI loading animation class object



def start_fim_daemon():
    try:
        event_handler = MyEventHandler()
        w_path_i = Path.cwd()
        w_path = w_path_i.resolve()
        observer = Observer()
        observer.schedule(event_handler, path=str(w_path), recursive=True)
        observer.start()

        with console.status(Fore.CYAN+"FIM Background Daemon running..."):
            while True:
                time.sleep(2)
    except KeyboardInterrupt:
        with console.status(Fore.RED+"Stopping Daemon.."):
            time.sleep(2)
        observer.stop()
    observer.join()




   











