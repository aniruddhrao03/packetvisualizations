import tkinter as tk
from tkinter import ttk
import socket
from threading import Thread

class PortScannerApp:
    def __init__(self, master):
        self.master = master
        master.title("CyberPort Scanner")
        master.configure(bg="#121212")

        self.style = ttk.Style()
        self.style.configure("TLabel", background="#121212", foreground="#56ff00", font=("Helvetica", 12))
        self.style.configure("TButton", background="#ff00ff", foreground="#000000", font=("Helvetica", 12))

        self.label_host = ttk.Label(master, text="Target Host:")
        self.label_host.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.entry_host = ttk.Entry(master, width=30)
        self.entry_host.grid(row=0, column=1, padx=10, pady=5)

        self.label_ports = ttk.Label(master, text="Port Range:")
        self.label_ports.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_ports = ttk.Entry(master, width=30)
        self.entry_ports.grid(row=1, column=1, padx=10, pady=5)

        self.button_scan = ttk.Button(master, text="Scan Ports", command=self.start_scan)
        self.button_scan.grid(row=2, columnspan=2, padx=10, pady=10)

        self.text_output = tk.Text(master, height=10, width=50)
        self.text_output.grid(row=3, columnspan=2, padx=10, pady=5)
        self.text_output.configure(bg="#000000", fg="#56ff00", font=("Courier", 10))

    def validate_port_range(self, port_range):
        try:
            start_port, end_port = map(int, port_range.split('-'))
            if start_port < 1 or start_port > 65535 or end_port < 1 or end_port > 65535 or start_port > end_port:
                return False
            return True
        except ValueError:
            return False

    def scan_port(self, target_host, target_port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_host, target_port))
            if result == 0:
                self.text_output.insert(tk.END, f"Port {target_port} is open\n", "open")
            else:
                self.text_output.insert(tk.END, f"Port {target_port} is closed\n", "closed")
            sock.close()
        except socket.error:
            self.text_output.insert(tk.END, "Couldn't connect to server\n", "error")

    def port_scan(self, target_host, port_range):
        start_port, end_port = map(int, port_range.split('-'))
        for port in range(start_port, end_port + 1):
            self.scan_port(target_host, port)

    def start_scan(self):
        target_host = self.entry_host.get()
        port_range = self.entry_ports.get()

        self.text_output.delete(1.0, tk.END)  # Clear previous output

        if not self.validate_port_range(port_range):
            self.text_output.insert(tk.END, "Invalid port range. Please enter a valid range (e.g., 1-65535).\n", "error")
            return

        self.text_output.insert(tk.END, f"Scanning {target_host}...\n", "info")

        scan_thread = Thread(target=self.port_scan, args=(target_host, port_range))
        scan_thread.start()

def main():
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
