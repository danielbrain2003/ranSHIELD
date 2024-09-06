import customtkinter as ctk
import subprocess
import platform
import socket
import psutil
import webbrowser
import ctypes
import os

# Function to fetch system information
def get_system_info():
    return {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "IPv4 Address": socket.gethostbyname(socket.gethostname())
    }

def get_cpu_usage():
    return {
        "CPU Usage (%)": f"{psutil.cpu_percent(interval=1)}%",
        "CPU Cores": psutil.cpu_count(logical=True)
    }

def get_memory_usage():
    mem = psutil.virtual_memory()
    return {
        "Total Memory (GB)": f"{mem.total / (1024 ** 3):.2f}",
        "Available Memory (GB)": f"{mem.available / (1024 ** 3):.2f}",
        "Used Memory (GB)": f"{mem.used / (1024 ** 3):.2f}",
        "Memory Usage (%)": f"{mem.percent}%"
    }

def get_network_info():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    net_io = psutil.net_io_counters()
    return {
        "Hostname": hostname,
        "Local IP": local_ip,
        "Bytes Sent (MB)": f"{net_io.bytes_sent / (1024 ** 2):.2f}",
        "Bytes Received (MB)": f"{net_io.bytes_recv / (1024 ** 2):.2f}"
    }

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return {
        "Total Disk (GB)": f"{disk.total / (1024 ** 3):.2f}",
        "Used Disk (GB)": f"{disk.used / (1024 ** 3):.2f}",
        "Free Disk (GB)": f"{disk.free / (1024 ** 3):.2f}",
        "Disk Usage (%)": f"{disk.percent}%"
    }

# Function to create a table frame for system information
def create_table_frame(parent, title, data):
    table_frame = ctk.CTkFrame(parent)
    table_frame.pack(fill="both", padx=10, pady=5)

    title_label = ctk.CTkLabel(table_frame, text=title, font=("Helvetica", 18, "bold"), anchor='w', text_color="skyblue")
    title_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=5)

    row = 1
    for key, value in data.items():
        key_label = ctk.CTkLabel(table_frame, text=key, font=("Helvetica", 14), anchor='w')
        key_label.grid(row=row, column=0, sticky='w', padx=5, pady=2)
        
        value_label = ctk.CTkLabel(table_frame, text=value, font=("Helvetica", 14), anchor='w')
        value_label.grid(row=row, column=1, sticky='w', padx=5, pady=2)
        
        row += 1

    return table_frame

class RanshieldApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RanSHIELD")
        self.geometry("900x500")

        # Create Navigation Menu
        self.nav_frame = ctk.CTkFrame(self, corner_radius=16, width=200, fg_color="#121212")
        self.nav_frame.grid(row=0, column=0, sticky="ns")

        self.content_frame = ctk.CTkFrame(self, corner_radius=16, fg_color="#F5F5F5")
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Buttons for Menu Navigation
        self.nav_buttons = [
            {"text": "Status", "command": self.show_status},
            {"text": "Protection", "command": self.show_protection},
            {"text": "Extortion", "command": self.show_extortion}
        ]

        for i, button in enumerate(self.nav_buttons):
            ctk.CTkButton(self.nav_frame, text=button["text"], font=("Roboto", 12), height=40, corner_radius=20,
                          command=button["command"]).grid(row=i, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(self.nav_frame, text="About", fg_color="#03DAC6", font=("Roboto", 12), height=40, corner_radius=20,
                      command=self.show_about).grid(row=len(self.nav_buttons), column=0, padx=20, pady=20, sticky="ew")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_status(self):
        self.clear_content_frame()
        self.show_system_info()

    def show_protection(self):
        self.clear_content_frame()
        protection_menu = PixelUIProtectionMenu(self.content_frame)
        protection_menu.pack(fill="both", expand=True)

    def show_extortion(self):
        self.clear_content_frame()
        extortion_frame = ExtortionMenu(self.content_frame)
        extortion_frame.pack(fill="both", expand=True)

    def show_about(self):
        self.clear_content_frame()

        # About Label
        about_label = ctk.CTkLabel(self.content_frame, text="RanSHIELD - Advanced Protection Suite\nVersion 1.0",
                               font=("Roboto", 18), text_color="#6200EE")
        about_label.pack(pady=10)

        # Additional Description
        description_label = ctk.CTkLabel(self.content_frame, text="RanSHIELD is a tool to monitor and secure your system against threats.",
                                     font=("Roboto", 14), text_color="#616161")
        description_label.pack(pady=5)

        # GitHub Link Description
        github_label = ctk.CTkLabel(self.content_frame, text="Click below to visit our GitHub page:", font=("Roboto", 14), text_color="#616161")
        github_label.pack(pady=5)
    
        # GitHub Button
        github_button = ctk.CTkButton(self.content_frame, text="Visit GitHub", fg_color="#03DAC6", font=("Roboto", 12),
                                  command=self.open_github)
        github_button.pack(pady=10)

    def open_github(self):
        webbrowser.open('https://github.com/TheBlackWolves/RanSHIELD')

    def show_system_info(self):
        categories = {
            "System Information": get_system_info(),
            "CPU Usage": get_cpu_usage(),
            "Memory Usage": get_memory_usage(),
            "Network Information": get_network_info(),
            "Disk Usage": get_disk_usage()
        }

        for title, data in categories.items():
            create_table_frame(self.content_frame, title, data)


class PixelUIProtectionMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=16, fg_color="#F5F5F5")
        self.configure(width=700, height=500)

        # Protection Menu Title
        self.title_label = ctk.CTkLabel(self, text="Protection", font=("Roboto", 24), text_color="#6200EE", anchor="center")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="n")

        self.subtitle_label = ctk.CTkLabel(self, text="Manage your system's protection", font=("Roboto", 14), text_color="#616161")
        self.subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="n")

        # Add a Pixel-inspired color bar
        self.color_bar = ctk.CTkFrame(self, height=4, width=600, fg_color="#6200EE", corner_radius=0)
        self.color_bar.grid(row=2, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        # Protection Items (File Monitor, Process Monitor, Network Shield, Authorized Installation)
        self.protection_items = [
            {"name": "File Monitor", "description": "Monitors system file activities", "script": r"C:\Users\Zoro\Videos\FileMonitor.exe"},
            {"name": "Process Monitor", "description": "Monitors suspicious processes", "script": r"C:\Users\Zoro\Videos\ProcessMonitoring.exe"},
            {"name": "Network Shield", "description": "Block Network when system compromised", "script": r"C:\Users\Zoro\Videos\NetworkShield.exe"},
            {"name": "Authorized Installation", "description": "Require password for installing applications", "script": r"C:\Users\Zoro\Videos\Authentication.exe"}
        ]

        self.switches = {}  # To keep track of the toggle switch states

        for idx, item in enumerate(self.protection_items):
            self.create_protection_item(item, idx)

        # Grid Configurations for Expansion
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def create_protection_item(self, item, index):
        """Create UI elements for each protection item."""
        row = 3 + index // 2
        col = index % 2

        # Item Frame
        item_frame = ctk.CTkFrame(self, corner_radius=16, width=300, height=150, fg_color="#FFFFFF", border_color="#DDDDDD", border_width=2)
        item_frame.grid(row=row, column=col, padx=20, pady=20, sticky="n")

        # Item Title
        item_title = ctk.CTkLabel(item_frame, text=item["name"], font=("Roboto", 18), text_color="#000000")
        item_title.pack(pady=10)

        # Item Description
        item_desc = ctk.CTkLabel(item_frame, text=item["description"], font=("Roboto", 12), text_color="#616161")
        item_desc.pack(pady=5)

        # Toggle Switch
        switch = ctk.CTkSwitch(item_frame, text="Enabled", onvalue=True, offvalue=False, command=lambda: self.toggle_protection_item(item))
        switch.pack(pady=10)

        # Store switch state to manage toggles
        self.switches[item["name"]] = switch

    def toggle_protection_item(self, item):
        """Toggle the protection item based on switch state."""
        switch = self.switches[item["name"]]
        if switch.get():
            self.activate_protection_item(item)
        else:
            self.deactivate_protection_item(item)

    def activate_protection_item(self, item):
        """Activates a protection item."""
        if "script" in item and os.path.isfile(item["script"]):
            self.open_file(item["script"])
        elif "function" in item:
            item["function"]()

    def deactivate_protection_item(self, item):
        """Deactivates a protection item."""
        # Placeholder for deactivation logic, if any.
        print(f"{item['name']} has been deactivated.")

    def open_file(self, file_path):
        """Open the specified file."""
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["start", file_path], shell=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", file_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", file_path])
        except Exception as e:
            print(f"Error opening file {file_path}: {e}")


class ExtortionMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=16, fg_color="#F5F5F5")
        self.configure(width=700, height=500)
        
        # Extortion Menu Title
        self.title_label = ctk.CTkLabel(self, text="Extortion", font=("Roboto", 24), text_color="#6200EE", anchor="center")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="n")

        self.subtitle_label = ctk.CTkLabel(self, text="Manage extortion threats", font=("Roboto", 14), text_color="#616161")
        self.subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="n")

        # Add a Pixel-inspired color bar
        self.color_bar = ctk.CTkFrame(self, height=4, width=600, fg_color="#6200EE", corner_radius=0)
        self.color_bar.grid(row=2, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        # Example Extortion Items
        self.extortion_items = [
            {"name": "File Encryption", "description": "Encrypts files to prevent unauthorized access"},
            {"name": "Ransom Note", "description": "Displays a ransom note to the victim"}
        ]

        for idx, item in enumerate(self.extortion_items):
            self.create_extortion_item(item, idx)

        # Grid Configurations for Expansion
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def create_extortion_item(self, item, index):
        """Create UI elements for each extortion item."""
        row = 3 + index // 2
        col = index % 2

        # Item Frame
        item_frame = ctk.CTkFrame(self, corner_radius=16, width=300, height=150, fg_color="#FFFFFF", border_color="#DDDDDD", border_width=2)
        item_frame.grid(row=row, column=col, padx=20, pady=20, sticky="n")

        # Item Title
        item_title = ctk.CTkLabel(item_frame, text=item["name"], font=("Roboto", 18), text_color="#000000")
        item_title.pack(pady=10)

        # Item Description
        item_desc = ctk.CTkLabel(item_frame, text=item["description"], font=("Roboto", 12), text_color="#616161")
        item_desc.pack(pady=5)

        # Action Button
        action_button = ctk.CTkButton(item_frame, text="Activate", command=lambda: self.activate_extortion_item(item))
        action_button.pack(pady=10)

    def activate_extortion_item(self, item):
        """Activates an extortion item."""
        print(f"Activating extortion item: {item['name']}")


if __name__ == "__main__":
    app = RanshieldApp()
    app.mainloop()
