import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import deque
import os

# Configuration
ENCRYPTION_THRESHOLD = 3  # Number of files to trigger the action
CHECK_INTERVAL = 1        # Time window in seconds
ENCRYPTED_EXTENSION = '.enc'  # Extension or marker for encrypted files

# Queue to store timestamps of file changes
file_changes = deque()

class EncryptionEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.event_type in ('modified', 'created'):
            # Record the timestamp of file changes
            file_changes.append(time.time())

def disable_network():
    try:
        # Get the list of network interfaces
        interfaces = subprocess.check_output(['netsh', 'interface', 'show', 'interface']).decode()
        # Iterate through the interfaces and disable each one
        for line in interfaces.splitlines():
            if 'Connected' in line:
                iface_name = line.split()[3]  # Adjust based on your netsh output format
                print(f"Disabling network interface: {iface_name}")
                subprocess.run(['netsh', 'interface', 'set', 'interface', iface_name, 'admin=disable'], check=True)
    except Exception as e:
        print(f"Failed to disable network: {e}")

def has_encrypted_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(ENCRYPTED_EXTENSION):
                return True
    return False

def monitor_system():
    event_handler = EncryptionEventHandler()
    observer = Observer()

    # Monitor C:\Users and C:\Windows\System32 directories
    observer.schedule(event_handler, path='C:\\Users', recursive=True)
    observer.schedule(event_handler, path='C:\\Windows\\System32', recursive=True)

    observer.start()

    try:
        while True:
            current_time = time.time()
            # Remove outdated file change events
            while file_changes and (current_time - file_changes[0] > CHECK_INTERVAL):
                file_changes.popleft()

            # Check if the number of recent changes exceeds the threshold
            if len(file_changes) > ENCRYPTION_THRESHOLD:
                print("High number of file changes detected. Checking for encrypted files...")
                # Check if there are encrypted files in the monitored directories
                if (has_encrypted_files('C:\\Users') or
                    has_encrypted_files('C:\\Windows\\System32')):
                    print("Encrypted files detected! Disabling network...")
                    disable_network()
                # Clear the changes after action is taken
                file_changes.clear()

            time.sleep(1)  # Check every second
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_system()
