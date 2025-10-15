#!/usr/bin/env python3
"""
D2L Class Buttons - Interactive class selection with button interface
Redesigned for cleaner, simpler workflow
"""

import time
import logging
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import asyncio
import threading
from playwright.async_api import async_playwright
import subprocess
import os

class D2LClassButtons:
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None
        self.logger = self.setup_logging()
        self.selected_class = None
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('d2l_class_buttons.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def setup_browser(self):
        """Launch Chrome directly with persistent profile (exactly like Interface-Project)"""
        try:
            # Use shared browser data directory
            browser_data_dir = os.path.abspath("../../Shared-Browser-Data/D2L-Macro-browser_data")
            os.makedirs(browser_data_dir, exist_ok=True)
            
            # Launch Chrome directly with command line (exactly like Interface-Project)
            chrome_cmd = f'start "" /max chrome --user-data-dir="{browser_data_dir}" --remote-debugging-port=9223 --window-position=100,100 --window-size=1920,1080 "{self.d2l_login_url}"'
            
            # Start Chrome process
            subprocess.Popen(chrome_cmd, shell=True)
            
            self.logger.info("Chrome browser launched successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to launch browser: {e}")
            return False

class D2LClassButtonsGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D2L Date Manager")
        self.root.geometry("450x320")
        self.root.resizable(False, False)
        
        # D2L Login URL
        self.d2l_login_url = "https://d2l.lonestar.edu/d2l/home"
        
        # Class URLs mapping
        self.class_urls = {
            "FM4202": "https://d2l.lonestar.edu/d2l/lms/manageDates/date_manager.d2l?fromCMC=1&ou=1580392",
            "FM4103": "https://d2l.lonestar.edu/d2l/lms/manageDates/date_manager.d2l?fromCMC=1&ou=1580390",
            "CA4203": "https://d2l.lonestar.edu/d2l/lms/manageDates/date_manager.d2l?fromCMC=1&ou=1580436",
            "CA4201": "https://d2l.lonestar.edu/d2l/lms/manageDates/date_manager.d2l?fromCMC=1&ou=1580434",
            "CA4105": "https://d2l.lonestar.edu/d2l/lms/manageDates/date_manager.d2l?fromCMC=1&ou=1580431",
        }
        
        # Variables
        self.csv_file_path = tk.StringVar()
        self.csv_data = None
        self.test = None
        self.logged_in = False
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="D2L Date Manager", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Login
        login_frame = ttk.LabelFrame(main_frame, text="Login", padding="8")
        login_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=3)
        
        self.login_btn = tk.Button(
            login_frame,
            text="Login to D2L",
            font=("Arial", 9, "bold"),
            bg="#2196F3",
            fg="white",
            width=15,
            height=1,
            command=self.login_to_d2l
        )
        self.login_btn.pack(pady=3)
        
        # Select Class
        class_frame = ttk.LabelFrame(main_frame, text="Select Class", padding="8")
        class_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=3)
        
        # Create smaller class buttons
        self.class_buttons = {}
        row = 0
        col = 0
        
        for class_name in self.class_urls.keys():
            btn = tk.Button(
                class_frame,
                text=class_name,
                font=("Arial", 8),
                width=9,
                height=1,
                relief="raised",
                bd=1,
                bg="#f5f5f5",
                activebackground="#e0e0e0",
                command=lambda name=class_name: self.go_to_class(name)
            )
            btn.grid(row=row, column=col, padx=4, pady=3)
            self.class_buttons[class_name] = btn
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Upload CSV
        csv_frame = ttk.LabelFrame(main_frame, text="Upload CSV", padding="8")
        csv_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=3)
        
        csv_inner_frame = ttk.Frame(csv_frame)
        csv_inner_frame.pack(fill=tk.X)
        
        csv_entry = ttk.Entry(csv_inner_frame, textvariable=self.csv_file_path, width=22, state="readonly")
        csv_entry.pack(side=tk.LEFT, padx=(0, 3))
        
        self.csv_browse_btn = ttk.Button(csv_inner_frame, text="Browse", command=self.browse_csv_file, width=7)
        self.csv_browse_btn.pack(side=tk.LEFT, padx=3)
        
        self.update_btn = tk.Button(
            csv_inner_frame,
            text="Update Dates",
            font=("Arial", 9, "bold"),
            bg="#4CAF50",
            fg="white",
            width=11,
            height=1,
            command=self.update_dates,
            state="disabled"
        )
        self.update_btn.pack(side=tk.LEFT, padx=3)
        
        ttk.Button(csv_inner_frame, text="Exit", command=self.exit_app, width=7).pack(side=tk.LEFT, padx=3)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready - Click 'Login to D2L' to begin", foreground="gray", font=("Arial", 8))
        self.status_label.grid(row=4, column=0, columnspan=3, pady=8)
        
        # Bottom button
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(3, 0))
        
        ttk.Button(button_frame, text="Clear Login", command=self.clear_login, width=12).pack()
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
    
    def login_to_d2l(self):
        """Open browser and navigate to D2L login"""
        try:
            self.status_label.config(text="Opening browser...", foreground="blue")
            
            # Initialize the browser
            self.test = D2LClassButtons()
            self.test.d2l_login_url = self.d2l_login_url
            
            if not self.test.setup_browser():
                self.status_label.config(text="Failed to open browser", foreground="red")
                messagebox.showerror("Error", "Failed to initialize browser")
                return
            
            self.logged_in = True
            self.status_label.config(text="Browser opened - Please log in manually", foreground="green")
            self.login_btn.config(state="disabled", bg="gray")
            
        except Exception as e:
            self.status_label.config(text="Login failed", foreground="red")
            messagebox.showerror("Error", f"Failed to open browser: {e}")
    
    def go_to_class(self, class_name):
        """Navigate to the selected class"""
        def run_async_navigation():
            async def async_navigation():
                try:
                    if not self.logged_in or not self.test or not self.test.page:
                        messagebox.showwarning("Not Logged In", "Please click 'Login to D2L' first!")
                        return
                    
                    class_url = self.class_urls.get(class_name)
                    if not class_url:
                        messagebox.showerror("Error", f"No URL found for class: {class_name}")
                        return
                    
                    # Reset all buttons
                    for btn in self.class_buttons.values():
                        btn.config(relief="raised", bg="#f5f5f5")
                    
                    # Highlight selected button
                    self.class_buttons[class_name].config(relief="sunken", bg="#90EE90")
                    
                    # Navigate to class
                    self.status_label.config(text=f"Navigating to {class_name}...", foreground="blue")
                    await self.test.page.goto(class_url)
                    await self.test.page.wait_for_load_state('networkidle')
                    self.test.selected_class = class_name
                    
                    self.status_label.config(text=f"Opened {class_name} - Upload CSV to continue", foreground="green")
                    
                    # Enable update button if CSV is loaded
                    if self.csv_file_path.get():
                        self.update_btn.config(state="normal")
                    
                except Exception as e:
                    self.status_label.config(text="Navigation failed", foreground="red")
                    messagebox.showerror("Error", f"Failed to navigate: {e}")
            
            # Run the async function in a new event loop
            asyncio.run(async_navigation())
        
        # Run the async function in a separate thread
        threading.Thread(target=run_async_navigation, daemon=True).start()
    
    def browse_csv_file(self):
        """Browse for CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_file_path.set(file_path)
            self.status_label.config(text="CSV loaded - Click 'Update Dates' to process", foreground="green")
            
            # Enable update button if we have a browser and class
            if self.logged_in and self.test and self.test.selected_class:
                self.update_btn.config(state="normal")
    
    def update_dates(self):
        """Process the CSV and update dates"""
        try:
            if not self.logged_in or not self.test or not self.test.driver:
                messagebox.showwarning("Not Logged In", "Please login first!")
                return
            
            if not self.test.selected_class:
                messagebox.showwarning("No Class", "Please select a class first!")
                return
            
            if not self.csv_file_path.get():
                messagebox.showwarning("No CSV", "Please select a CSV file first!")
                return
            
            self.status_label.config(text="Processing CSV...", foreground="blue")
            
            # Read CSV
            try:
                self.csv_data = pd.read_csv(self.csv_file_path.get())
            except Exception as e:
                messagebox.showerror("CSV Error", f"Error reading CSV: {e}")
                return
            
            # Import and run CSV processor
            from d2l_date_processing import D2LDateProcessor
            
            csv_processor = D2LDateProcessor()
            csv_processor.driver = self.test.driver
            csv_processor.logger = self.test.logger
            
            processed, errors = csv_processor.process_csv_file(self.csv_file_path.get())
            
            if errors == 0:
                self.status_label.config(text=f"Success! Processed {processed} assignments", foreground="green")
                messagebox.showinfo("Success", f"Successfully processed {processed} assignments!")
            else:
                self.status_label.config(text=f"Completed: {processed} processed, {errors} errors", foreground="orange")
                messagebox.showwarning("Completed", f"Processed {processed}, but {errors} had errors.")
            
        except Exception as e:
            self.status_label.config(text="Processing failed", foreground="red")
            messagebox.showerror("Error", f"Failed to process: {e}")
    
    def clear_login(self):
        """Clear saved login data"""
        try:
            import shutil
            import tempfile
            profile_dir = os.path.join(tempfile.gettempdir(), "d2l_chrome_profile")
            if os.path.exists(profile_dir):
                shutil.rmtree(profile_dir)
                messagebox.showinfo("Success", "Login data cleared")
            else:
                messagebox.showinfo("Info", "No login data to clear")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear login: {e}")
    
    def exit_app(self):
        """Exit the application"""
        try:
            if self.test and self.test.context:
                # Don't close the browser - let it stay open like the makeup exam macro
                pass
        except:
            pass
        self.root.quit()
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def cleanup_existing_processes():
    """Clean up any existing Chrome processes"""
    try:
        subprocess.run(["taskkill", "/f", "/im", "chromedriver.exe"], capture_output=True)
        subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], capture_output=True)
    except:
        pass

def main():
    """Main function"""
    cleanup_existing_processes()
    app = D2LClassButtonsGUI()
    app.run()

if __name__ == "__main__":
    main()