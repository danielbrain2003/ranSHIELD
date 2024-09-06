import os
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, directory_path):
        self.directory_path = directory_path
    
    def on_modified(self, event):
        print(f"File modified: {event.src_path}")
        self.kill_all_processes()

    def on_deleted(self, event):
        print(f"File deleted: {event.src_path}")
        self.kill_all_processes()

    def on_created(self, event):
        print(f"File created: {event.src_path}")
        self.kill_all_processes()

    def on_moved(self, event):
        print(f"File moved: {event.src_path}")
        self.kill_all_processes()
            
    def kill_all_processes(self):
        print("Killing all processes...")
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Skip killing the current process
                if proc.pid == os.getpid():
                    continue
                proc.terminate()
                proc.wait(timeout=3)  # Wait for the process to terminate
                print(f"Killed process: {proc.info['name']} (PID: {proc.info['pid']})")
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                print(f"Access denied to terminate process: {proc.info['name']} (PID: {proc.info['pid']})")
            except psutil.TimeoutExpired:
                print(f"Timed out waiting for process to terminate: {proc.info['name']} (PID: {proc.info['pid']})")

def main():
    directory_path = input("Enter the path of the directory to monitor: ")
    
    if not os.path.isdir(directory_path):
        print(f"The specified directory does not exist: {directory_path}")
        return

    event_handler = FileMonitorHandler(directory_path)
    observer = Observer()
    observer.schedule(event_handler, path=directory_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
