import os
import hashlib
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DirectoryMonitorHandler(FileSystemEventHandler):
    def __init__(self):
        self.file_checksums = {}

    def on_modified(self, event):
        if event.is_directory:
            return
        self.check_file_accessed_or_encrypted(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self.check_file_accessed_or_encrypted(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        self.check_file_accessed_or_encrypted(event.dest_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f"File deleted: {event.src_path}. Shutting down the system...")
        self.shutdown_system()

    def check_file_accessed_or_encrypted(self, file_path):
        current_checksum = self.get_file_checksum(file_path)
        previous_checksum = self.file_checksums.get(file_path)
        if previous_checksum is not None and current_checksum != previous_checksum:
            print(f"File accessed or encrypted: {file_path}. Shutting down the system...")
            self.shutdown_system()
        self.file_checksums[file_path] = current_checksum

    def get_file_checksum(self, file_path):
        if not os.path.isfile(file_path):
            return None
        hash_algo = hashlib.sha256()
        try:
            with open(file_path, 'rb') as file:
                while chunk := file.read(4096):
                    hash_algo.update(chunk)
            return hash_algo.hexdigest()
        except Exception as e:
            print(f"Error calculating checksum for {file_path}: {e}")
            return None

    def shutdown_system(self):
        print("Shutting down the system...")
        if os.name == 'nt':
            subprocess.run(["shutdown", "/s", "/t", "0"])
        elif os.name == 'posix':
            subprocess.run(["sudo", "shutdown", "-h", "now"])
        else:
            print("Unsupported OS")

def monitor_directory(directory_path):
    event_handler = DirectoryMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_path, recursive=True)
    observer.start()
    print(f"Monitoring directory {directory_path}. Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directory_path = input("Enter the path of the directory to monitor: ").strip()

    if not os.path.isdir(directory_path):
        print(f"Error: The directory {directory_path} does not exist.")
    else:
        monitor_directory(directory_path)
