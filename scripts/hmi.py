import tkinter as tk
from tkinter import ttk
import socket
import os

class HMIApp:
    def __init__(self, root, program):
        self.program = program
        self.root = root
        self.root.title("Raspberry Pi HMI")
        self.root.geometry("480x800")  # Common Raspberry Pi touchscreen resolution
        self.root.configure(bg="#2c3e50")  # Dark blue background

        # Style configuration
        style = ttk.Style()
        style.configure("Big.TButton", font=("Arial", 36), padding=30, background="#2D4231", foreground="#ffffff")
        style.configure("Batch.TButton", font=("Arial", 36), padding=30, background="#3498db", foreground="#ffffff")
        style.configure("Big.TLabel", font=("Arial", 42), background="#2c3e50", foreground="#ecf0f1")
        style.configure("Medium.TLabel", font=("Arial", 32), background="#2c3e50", foreground="#ecf0f1")
        style.configure("Small.TLabel", font=("Arial", 16), background="#2c3e50", foreground="#ecf0f1")
        style.configure("Thick.Horizontal.TProgressbar", troughcolor="#34495e", background="#2ecc71", thickness=50)

        # System Status Button
        self.status_button = ttk.Button(root, text="sytm_is_stopped", command=self.toggle_status, style="Big.TButton")
        self.status_button.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        # Counter and Batch Size Label
        self.counter_label = ttk.Label(root, text="Counter: 0/10", style="Big.TLabel")
        self.counter_label.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        # Total Counts Label (smaller font)
        self.total_counts_label = ttk.Label(root, text="Total Counts: 0", style="Medium.TLabel")
        self.total_counts_label.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        # Progress Bar
        self.progress = ttk.Progressbar(root, length=700, mode='determinate', style="Thick.Horizontal.TProgressbar")
        self.progress.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        # Batch Size Buttons
        self.batch_size_10 = ttk.Button(root, text="10", command=lambda: self.update_batch_size(10), style="Batch.TButton")
        self.batch_size_10.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")

        self.batch_size_15 = ttk.Button(root, text="15", command=lambda: self.update_batch_size(15), style="Batch.TButton")
        self.batch_size_15.grid(row=4, column=1, padx=20, pady=20, sticky="nsew")

        # IP Address Label (bottom-left corner)
        self.ip_label = ttk.Label(root, text=f"IP: {self.get_ip_address()}", style="Small.TLabel")
        self.ip_label.grid(row=5, column=0, padx=10, pady=10, sticky="sw")

        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)

        # Start periodic UI update
        self.update_ui()

    def get_ip_address(self):
        """Get the Raspberry Pi's IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Unknown"

    def toggle_status(self):
        self.program.toggle_running()
        self.status_button.config(text="sytm_is_running" if self.program.is_running else "sytm_is_stopped")

    def update_batch_size(self, size):
        self.program.batch_size = size

    def update_ui(self):
        self.counter_label.config(text=f"Counter: {self.program.counter}/{self.program.batch_size}")
        self.total_counts_label.config(text=f"Total Counts: {self.program.total_counts}")
        percentage = (self.program.counter / self.program.batch_size) * 100 if self.program.batch_size > 0 else 0
        self.progress['value'] = percentage
        self.root.after(500, self.update_ui)  # Update every 500ms