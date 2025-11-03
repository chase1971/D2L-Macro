#===============================================================================
# CODE SYNOPSIS: d2l_date_processing.py
# SYNOPSIS_HASH: a681c15a961b4b1288763f26391813c9f1d705c3e077f97608edae6b702682fd
# Generated: 2025-10-25 14:48:11
# INTENT: D2L assignment date automation and management.
#===============================================================================
#
# OVERVIEW:
#   Total Lines: 1115
#   Functions: 21
#   Classes: 2
#   Global Variables: 0
#
# Key Dependencies:
#   - csv
#   - datetime
#   - logging
#   - os
#   - psutil
#   - re
#   - selenium
#   - selenium.common.exceptions
#   - selenium.webdriver.chrome.options
#   - selenium.webdriver.chrome.service
#   - selenium.webdriver.common.by
#   - selenium.webdriver.support
#   - selenium.webdriver.support.ui
#   - shutil
#   - subprocess
#   - tempfile
#   - threading
#   - time
#   - tkinter
#   - webdriver_manager.chrome
#
#===============================================================================
# ════════════════════
# BEGIN MACHINE-READABLE DATA (for automated processing)
# ════════════════════
# SYNOPSIS_ANNOTATED: YES
# LAST_ANALYZED: 2025-10-25 14:48:11
# FILE: d2l_date_processing.py
# IMPORTS_EXTERNAL: csv, datetime, logging, os, psutil, re, selenium, selenium.common.exceptions, selenium.webdriver.chrome.options, selenium.webdriver.chrome.service, selenium.webdriver.common.by, selenium.webdriver.support, selenium.webdriver.support.ui, shutil, subprocess, tempfile, threading, time, tkinter, webdriver_manager.chrome
# IMPORTS_LOCAL: 
# GLOBALS: 
# FUNCTIONS: __init__, browse_csv_file, cleanup_existing_processes, clear_login, create_widgets, exit_app, find_assignment_due_date_link, find_assignment_start_date_link, login_to_d2l, main, process_csv, process_csv_file, run, set_assignment_due_date, set_assignment_start_date, set_date_in_iframe, set_date_in_mini_editor, set_start_date_in_mini_editor, setup_driver, setup_logging, update_status
# RETURNS: find_assignment_due_date_link, find_assignment_start_date_link, process_csv_file, set_assignment_due_date, set_assignment_start_date, set_date_in_iframe, set_date_in_mini_editor, set_start_date_in_mini_editor, setup_driver, setup_logging
# THREAD_TARGETS: 
# HOTKEYS: 
# TK_BINDS: 
# COMMAND_BINDS: 
# CLASSES: D2LDateProcessor, D2LDateProcessorGUI
# IO_READS: unknown
# IO_WRITES: 
# EXCEPTIONS: line 1088: ['all exceptions'], line 51: ['Exception'], line 96: ['Exception'], line 199: ['Exception'], line 222: ['Exception'], line 261: ['Exception'], line 406: ['Exception'], line 557: ['Exception'], line 608: ['Exception'], line 681: ['Exception'], line 1001: ['Exception'], line 1025: ['Exception'], line 1051: ['Exception'], line 1073: ['all exceptions'], line 1089: ['ImportError'], line 74: ['Exception'], line 233: ['Exception'], line 685: ['Exception'], line 730: ['Exception'], line 860: ['Exception'], line 600: ['all exceptions'], line 624: ['all exceptions'], line 673: ['all exceptions'], line 892: ['all exceptions'], line 1095: ['all exceptions'], line 113: ['Exception'], line 239: ['Exception'], line 281: ['all exceptions'], line 317: ['all exceptions'], line 373: ['Exception'], line 428: ['all exceptions'], line 466: ['all exceptions'], line 489: ['Exception'], line 528: ['Exception'], line 871: ['all exceptions'], line 745: ['Exception'], line 765: ['Exception'], line 146: ['Exception']
# CALLGRAPH_ROOTS: main,__init__,setup_logging,setup_driver,process_csv_file,set_assignment_due_date,set_assignment_start_date,find_assignment_due_date_link,find_assignment_start_date_link,set_date_in_mini_editor,set_start_date_in_mini_editor,set_date_in_iframe,create_widgets,browse_csv_file,update_status,login_to_d2l,process_csv,clear_login,exit_app,run
# STATE_VARS: 
# STATE_MACHINES_COUNT: 0
# STATE_TRANSITIONS_COUNT: 0
# INIT_SEQUENCE: 
# INTENT: D2L assignment date automation and management.
# FUNCTION_INTENTS: __init__=Handles the target entities., browse_csv_file=Browse for CSV file., cleanup_existing_processes=Clean up any existing Chrome/ChromeDriver processes., clear_login=Clear saved login session., create_widgets=Create the GUI widgets., exit_app=Exit the application., find_assignment_due_date_link=Find the due date link for a specific assignment by name with fuzzy matching., find_assignment_start_date_link=Find the start date link for a specific assignment by name with fuzzy matching., login_to_d2l=Handle login process., main=Main function., process_csv=Process the CSV file., process_csv_file=Process CSV file and update assignments., run=Start the GUI., set_assignment_due_date=Set due date for a specific assignment., set_assignment_start_date=Set start date for a specific assignment., set_date_in_iframe=Set date and time in the iframe., set_date_in_mini_editor=Set date and time in the mini editor popup., set_start_date_in_mini_editor=Set start date in mini editor - handles start date checkbox., setup_driver=Setup Chrome driver with persistent login session., setup_logging=Setup logging configuration., update_status=Update the status label and log.
# END MACHINE-READABLE DATA
# ════════════════════
#===============================================================================
#
# 📝 FUNCTION SIGNATURES:
#
# D2LDateProcessor.__init__(self) -> None
#
# D2LDateProcessor.find_assignment_due_date_link(self, assignment_name) -> None
#   Find the due date link for a specific assignment by name with fuzzy matching
#
# D2LDateProcessor.find_assignment_start_date_link(self, assignment_name) -> None
#   Find the start date link for a specific assignment by name with fuzzy matching
#
# D2LDateProcessor.process_csv_file(self, csv_file_path) -> None
#   Process CSV file and update assignments
#
# D2LDateProcessor.set_assignment_due_date(self, assignment_name, due_date, due_time) -> None
#   Set due date for a specific assignment
#
# D2LDateProcessor.set_assignment_start_date(self, assignment_name, start_date, start_time) -> None
#   Set start date for a specific assignment
#
# D2LDateProcessor.set_date_in_iframe(self, new_date, new_time, checkbox_id = None) -> None
#   Set date and time in the iframe
#
# D2LDateProcessor.set_date_in_mini_editor(self, new_date, new_time) -> None
#   Set date and time in the mini editor popup
#
# D2LDateProcessor.set_start_date_in_mini_editor(self, new_date, new_time) -> None
#   Set start date in mini editor - handles start date checkbox
#
# D2LDateProcessor.setup_driver(self, use_profile = True) -> None
#   Setup Chrome driver with persistent login session
#
# D2LDateProcessor.setup_logging(self) -> None
#   Setup logging configuration
#
# D2LDateProcessorGUI.__init__(self) -> None
#
# D2LDateProcessorGUI.browse_csv_file(self) -> None
#   Browse for CSV file
#
# D2LDateProcessorGUI.clear_login(self) -> None
#   Clear saved login session
#
# D2LDateProcessorGUI.create_widgets(self) -> None
#   Create the GUI widgets
#
# D2LDateProcessorGUI.exit_app(self) -> None
#   Exit the application
#
# D2LDateProcessorGUI.login_to_d2l(self) -> None
#   Handle login process
#
# D2LDateProcessorGUI.process_csv(self) -> None
#   Process the CSV file
#
# D2LDateProcessorGUI.run(self) -> None
#   Start the GUI
#
# D2LDateProcessorGUI.update_status(self, message) -> None
#   Update the status label and log
#
# cleanup_existing_processes() -> None
#   Clean up any existing Chrome/ChromeDriver processes
#
# main() -> None
#   Main function
#
#===============================================================================
#
# 🧱 CLASSES FOUND:
#
#   D2LDateProcessor (line 28):
#     - D2LDateProcessor.__init__()
#     - D2LDateProcessor.setup_logging()
#     - D2LDateProcessor.setup_driver()
#     - D2LDateProcessor.process_csv_file()
#     - D2LDateProcessor.set_assignment_due_date()
#     - D2LDateProcessor.set_assignment_start_date()
#     - D2LDateProcessor.find_assignment_due_date_link()
#     - D2LDateProcessor.find_assignment_start_date_link()
#     - D2LDateProcessor.set_date_in_mini_editor()
#     - D2LDateProcessor.set_start_date_in_mini_editor()
#     - D2LDateProcessor.set_date_in_iframe()
#   D2LDateProcessorGUI (line 899):
#     - D2LDateProcessorGUI.__init__()
#     - D2LDateProcessorGUI.create_widgets()
#     - D2LDateProcessorGUI.browse_csv_file()
#     - D2LDateProcessorGUI.update_status()
#     - D2LDateProcessorGUI.login_to_d2l()
#     - D2LDateProcessorGUI.process_csv()
#     - D2LDateProcessorGUI.clear_login()
#     - D2LDateProcessorGUI.exit_app()
#     - D2LDateProcessorGUI.run()
#===============================================================================
#
# 🧠 FUNCTION BEHAVIORAL SUMMARIES:
#
#
#===============================================================================
#
# FUNCTION CALL HIERARCHY (depth-limited):
#
# - main()
#
# - __init__()
#
# - setup_logging()
#
# - setup_driver()
#
# - process_csv_file()
#
# - set_assignment_due_date()
#
# - set_assignment_start_date()
#
# - find_assignment_due_date_link()
#
# - find_assignment_start_date_link()
#
# - set_date_in_mini_editor()
#
# - set_start_date_in_mini_editor()
#
# - set_date_in_iframe()
#
# - create_widgets()
#
# - browse_csv_file()
#
# - update_status()
#
# - login_to_d2l()
#
# - process_csv()
#
# - clear_login()
#
# - exit_app()
#
# - run()
#
#===============================================================================
#
# 🔄 STATE MACHINES:
#
#   (No state machines detected.)
#
#===============================================================================
#
# 🔌 EXTERNAL I/O SUMMARY:
#
#   Reads: unknown
#===============================================================================
#
# 📊 DATA FLOW SUMMARY:
#
#   setup_logging() — calls logging.FileHandler, logging.StreamHandler, logging.basicConfig, logging.getLogger, os.makedirs; returns value
#   setup_driver() — calls ChromeDriverManager, Options, Service, chrome_options.add_argument, chrome_options.add_experimental_option, install; returns value
#   process_csv_file() — calls ValueError, all, assignment_name.strip, bool, csv.DictReader, enumerate; returns value
#   set_assignment_due_date() — calls due_date_link.click, result.get, self.driver.execute_script, self.find_assignment_due_date_link, self.logger.error, self.logger.info; returns value
#   set_assignment_start_date() — calls result.get, self.driver.execute_script, self.find_assignment_start_date_link, self.logger.error, self.logger.info, self.logger.warning; returns value
#   find_assignment_due_date_link() — calls any, assignment_cell.find_element, assignment_link.find_element, assignment_name.replace, cell.find_elements, date_links.append; returns value
#   find_assignment_start_date_link() — calls any, assignment_cell.find_element, assignment_link.find_element, assignment_name.replace, cell.find_elements, enumerate; returns value
#   set_date_in_mini_editor() — calls EC.presence_of_element_located, WebDriverWait, dialog.find_elements, enumerate, len, self.driver.execute_script; returns value
#   set_start_date_in_mini_editor() — calls EC.presence_of_element_located, WebDriverWait, enumerate, len, self.driver.execute_script, self.driver.find_elements; returns value
#   set_date_in_iframe() — calls checkbox.click, checkbox.is_selected, checkbox_result.get, datetime.strptime, int, new_date.split; returns value
#   __init__() — calls self.create_widgets, self.root.geometry, self.root.title, tk.Tk; no return value
#   create_widgets() — calls button_frame.grid, csv_frame.columnconfigure, csv_frame.grid, grid, main_frame.columnconfigure, main_frame.grid; no return value
#   browse_csv_file() — calls filedialog.askopenfilename, os.path.basename, self.csv_label.config, self.csv_var.set, self.update_status; no return value
#   update_status() — calls self.log_text.insert, self.log_text.see, self.root.update, self.status_var.set; no return value
#   login_to_d2l() — calls D2LDateProcessor, hasattr, self.automation.driver.get, self.automation.setup_driver, self.process_button.config, self.update_status; no return value
#   process_csv() — calls messagebox.showerror, messagebox.showinfo, messagebox.showwarning, self.automation.process_csv_file, self.update_status; no return value
#   clear_login() — calls hasattr, os.path.exists, os.path.join, self.automation.driver.quit, self.process_button.config, self.update_status; no return value
#   exit_app() — calls hasattr, self.automation.driver.quit, self.root.destroy; no return value
#   run() — calls self.root.mainloop; no return value
#   cleanup_existing_processes() — calls proc.kill, psutil.process_iter, subprocess.run; no return value
#   main() — calls D2LDateProcessorGUI, app.run, cleanup_existing_processes, print; no return value
#===============================================================================
#
# 🔧 MODULARIZATION RECOMMENDATIONS:
#
# When modularizing, consider splitting by:
#   - Separate state management from business logic
#   - Group related functions into modules
#   - Separate UI code from core logic
#===============================================================================
#===============================================================================
# 📞 FUNCTION CALL HIERARCHY:
#   (No intra-module function calls detected.)
#===============================================================================
# 🔄 STATE MACHINE TRANSITIONS:
#   (No *_state transitions detected.)
#===============================================================================
# ⌨️ HOTKEY BINDINGS:
#   (No keyboard hotkeys detected.)
#===============================================================================
#
# 🧩 MODULE INTEGRATION INTENT:
#   Role: Single-file code analyzer that injects a synopsis header
#   Used by: (future) system_synopsis_builder.py for folder-wide Markdown
#   Inputs: Python source file path
#   Outputs: Annotated source file (prepends this synopsis)
#===============================================================================
#
# 📝 INSTRUCTIONS FOR AI:
#   1. Preserve ALL global variable dependencies shown above
#   2. Maintain thread safety for variables accessed by multiple threads
#   3. Do NOT rename variables unless explicitly asked
#   4. Ensure all function dependencies are preserved
#   5. Keep UI-threaded calls (e.g., tk.after) on main thread or marshal via queue
#   6. Ensure hotkeys and binds still invoke the same callbacks
#===============================================================================
# === END SYNOPSIS HEADER ===
# === END SYNOPSIS HEADER ===
# === END SYNOPSIS HEADER ===
# === END SYNOPSIS HEADER ===
# === END SYNOPSIS HEADER ===
#!/usr/bin/env python3
"""
D2L Date Processor - Bulk Date Assignment Editor with CSV Support
Reads assignment names and dates from a CSV file and automatically updates them in D2L.
"""

import time
import logging
import os
import subprocess
import shutil
import csv
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class D2LDateProcessor:
    def __init__(self):
        self.driver = None
        self.logger = self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/d2l_date_processing.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
        
    def setup_driver(self, use_profile=True):
        """Setup Chrome driver with persistent login session"""
        try:
            from selenium.webdriver.chrome.options import Options
            
            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            
            if use_profile:
                # Use persistent profile for login session
                import tempfile
                profile_dir = os.path.join(tempfile.gettempdir(), "d2l_chrome_profile")
                self.logger.info(f"Using persistent profile: {profile_dir}")
                chrome_options.add_argument(f"--user-data-dir={profile_dir}")
                chrome_options.add_argument("--profile-directory=D2L_Profile")
            
            # Force browser to open on secondary monitor (left side, 2K resolution)
            chrome_options.add_argument("--window-position=-1920,0")  # Left monitor position
            chrome_options.add_argument("--window-size=1920,1080")    # 2K resolution
            
            # Try ChromeDriverManager first, then fallback
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.logger.info("Chrome driver created successfully (ChromeDriverManager)")
            except Exception as e:
                self.logger.warning(f"ChromeDriverManager failed: {e}")
                # Fallback to system chromedriver
                self.driver = webdriver.Chrome(options=chrome_options)
                self.logger.info("Chrome driver created successfully (direct)")
            
            # Execute script to hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("Chrome driver setup completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome driver: {e}")
            return False
    
    def process_csv_file(self, csv_file_path):
        """Process CSV file and update assignments"""
        try:
            self.logger.info(f"Processing CSV file: {csv_file_path}")
            
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Validate CSV headers - UPDATED FOR USER'S EXACT FORMAT
                required_headers = ['Name', 'Start Date', 'Start Time', 'Due Date', 'Due Time']
                if not all(header in reader.fieldnames for header in required_headers):
                    raise ValueError(f"CSV must have required headers: {required_headers}")
                
                self.logger.info(f"CSV headers found: {reader.fieldnames}")
                
                processed_count = 0
                error_count = 0
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 because row 1 is headers
                    try:
                        assignment_name = row['Name'].strip()
                        if not assignment_name:
                            self.logger.warning(f"Row {row_num}: Empty assignment name, skipping")
                            continue
                        
                        # DEBUG: Show exactly what we're searching for
                        self.logger.info(f"Row {row_num}: Processing assignment name: '{assignment_name}'")
                        self.logger.info(f"Assignment name length: {len(assignment_name)} characters")
                        self.logger.info(f"Assignment name repr: {repr(assignment_name)}")
                        
                        # Clean the assignment name of quotes
                        clean_assignment_name = assignment_name.strip('"').strip("'").strip()
                        if clean_assignment_name != assignment_name:
                            self.logger.info(f"Cleaned assignment name: '{clean_assignment_name}'")
                        
                        # Process due date FIRST (to avoid D2L validation errors)
                        start_success = False
                        due_success = False
                        
                        due_date = row['Due Date'].strip()
                        due_time = row['Due Time'].strip()
                        
                        # ENHANCED DEBUG: Show ALL CSV values
                        self.logger.info(f"DEBUG: ALL CSV ROW VALUES:")
                        for key, value in row.items():
                            self.logger.info(f"  '{key}': '{value}' (len={len(value)})")
                        
                        self.logger.info(f"DEBUG: Raw due_date='{due_date}', due_time='{due_time}'")
                        self.logger.info(f"DEBUG: due_date bool={bool(due_date)}, due_time bool={bool(due_time)}")
                        
                        if due_date and due_time:
                            self.logger.info(f"CONDITION MET: Setting due date: {due_date} at {due_time}")
                            try:
                                if self.set_assignment_due_date(clean_assignment_name, due_date, due_time):
                                    self.logger.info("Due date set successfully!")
                                    due_success = True
                                else:
                                    self.logger.error("Failed to set due date")
                                    error_count += 1
                            except Exception as e:
                                self.logger.error(f"EXCEPTION during due date processing: {e}")
                                error_count += 1
                        else:
                            self.logger.warning(f"SKIPPING due date - due_date='{due_date}' ({bool(due_date)}), due_time='{due_time}' ({bool(due_time)})")
                        
                        # Ensure we're back on the main page before processing start date
                        if due_success:
                            self.logger.info("Returning to main page before processing start date...")
                            time.sleep(0.5)  # Wait for any page transitions
                        
                        # Process start date SECOND (after due date to avoid validation errors)
                        start_date = row['Start Date'].strip()
                        start_time = row['Start Time'].strip()
                        
                        if start_date and start_time:
                            self.logger.info(f"Setting start date: {start_date} at {start_time}")
                            if self.set_assignment_start_date(clean_assignment_name, start_date, start_time):
                                self.logger.info("Start date set successfully!")
                                start_success = True
                            else:
                                self.logger.error("Failed to set start date")
                                error_count += 1
                        
                        # Count as successful if at least one date was set
                        if start_success or due_success:
                            processed_count += 1
                            self.logger.info(f"Successfully processed '{clean_assignment_name}'")
                        
                        # Small delay between assignments
                        time.sleep(0.5)
                        
                    except Exception as e:
                        self.logger.error(f"Error processing row {row_num}: {e}")
                        error_count += 1
                        continue
                
                self.logger.info(f"CSV processing completed: {processed_count} successful, {error_count} errors")
                return processed_count, error_count
                
        except Exception as e:
            self.logger.error(f"Error processing CSV file: {e}")
            return 0, 1
    
    def set_assignment_due_date(self, assignment_name, due_date, due_time):
        """Set due date for a specific assignment"""
        try:
            # Find and click the due date link
            due_date_link = self.find_assignment_due_date_link(assignment_name)
            if not due_date_link:
                return False
            
            # Click the due date link
            self.driver.execute_script("arguments[0].scrollIntoView(true);", due_date_link)
            time.sleep(0.5)
            due_date_link.click()
            self.logger.info("Clicked due date link")
            time.sleep(2)
            
            # Set the date in the mini editor
            result = self.set_date_in_mini_editor(due_date, due_time)
            return result.get('dateSet', False) or result.get('timeSet', False)
            
        except Exception as e:
            self.logger.error(f"Error setting due date for '{assignment_name}': {e}")
            return False
    
    def set_assignment_start_date(self, assignment_name, start_date, start_time):
        """Set start date for a specific assignment"""
        try:
            # Find and click the start date link
            start_date_link = self.find_assignment_start_date_link(assignment_name)
            if not start_date_link:
                return False
            
            # Click the start date link with multiple methods
            self.driver.execute_script("arguments[0].scrollIntoView(true);", start_date_link)
            time.sleep(0.5)
            
            self.logger.info("Attempting to click start date link...")
            try:
                # Method 1: Regular click
                start_date_link.click()
                self.logger.info("SUCCESS: Selenium click on start date link executed")
            except Exception as e:
                self.logger.warning(f"Selenium click failed: {e}")
                try:
                    # Method 2: JavaScript click
                    self.driver.execute_script("arguments[0].click();", start_date_link)
                    self.logger.info("SUCCESS: JavaScript click on start date link executed")
                except Exception as e2:
                    self.logger.error(f"JavaScript click also failed: {e2}")
                    return False
            
            # Wait longer for the start date editor to appear
            self.logger.info("Waiting for start date mini-editor to load...")
            time.sleep(3)  # Increased wait time
            
            # Set the date in the mini editor (with start date checkbox)
            result = self.set_start_date_in_mini_editor(start_date, start_time)
            return result.get('dateSet', False) or result.get('timeSet', False)
            
        except Exception as e:
            self.logger.error(f"Error setting start date for '{assignment_name}': {e}")
            return False
    
    def _remove_emojis(self, text: str) -> str:
        """
        Remove emojis and other emoji-related Unicode characters from a string.
        
        Parameters
        ----------
        text : str
            The text to clean.
            
        Returns
        -------
        str
            The text with emojis removed.
        """
        import re
        # Remove emojis and emoji-related Unicode ranges
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Misc Symbols and Pictographs
            "\U0001F680-\U0001F6FF"  # Transport and Map
            "\U0001F1E0-\U0001F1FF"  # Flags
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"  # Enclosed characters
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002600-\U000026FF"  # Miscellaneous Symbols
            "\U00002700-\U000027BF"  # Dingbats
            "\U0000FE00-\U0000FE0F"  # Variation Selectors
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub('', text).strip()

    def find_assignment_due_date_link(self, assignment_name):
        """Find the due date link for a specific assignment by name with fuzzy matching"""
        try:
            self.logger.info(f"Looking for due date link for assignment: '{assignment_name}'")
            
            # Strategy 1: Exact match - try multiple variations
            self.logger.info(f"Searching for EXACT match: '{assignment_name}'")
            
            # Try exact match first
            assignment_links = self.driver.find_elements(By.XPATH, f"//a[contains(text(), '{assignment_name}')]")
            
            # If no exact match, try normalized matching (remove dashes, normalize commas, remove emojis)
            if not assignment_links:
                # Normalize search term: remove dashes, normalize comma spacing, collapse spaces
                import re
                name_normalized = re.sub(r'[-–—−]', ' ', assignment_name)  # Replace dashes with spaces
                name_normalized = re.sub(r',\s*', ', ', name_normalized)  # Normalize comma spacing to ", "
                name_normalized = re.sub(r'\s+', ' ', name_normalized).strip()  # Collapse multiple spaces
                name_normalized = self._remove_emojis(name_normalized)  # Remove emojis
                name_normalized_lower = name_normalized.lower()
                self.logger.info(f"Trying normalized search: '{name_normalized}'")
                
                # Find all links and check their text with the same normalization
                all_links = self.driver.find_elements(By.XPATH, "//td[contains(@class, 'd_dg_col_Name')]//a")
                for link in all_links:
                    try:
                        link_text = link.text.strip()
                        link_normalized = re.sub(r'[-–—−]', ' ', link_text)  # Replace dashes with spaces
                        link_normalized = re.sub(r',\s*', ', ', link_normalized)  # Normalize comma spacing to ", "
                        link_normalized = re.sub(r'\s+', ' ', link_normalized).strip()  # Collapse multiple spaces
                        link_normalized = self._remove_emojis(link_normalized)  # Remove emojis
                        link_normalized_lower = link_normalized.lower()
                        
                        # EXACT MATCH ONLY after normalization - prevents confusion between similar assignments
                        if name_normalized_lower == link_normalized_lower:
                            self.logger.info(f"SUCCESS: Found exact normalized match! '{link_text}'")
                            assignment_links = [link]
                            break
                    except:
                        continue
            
            # If still no match, try without quotes and emojis
            if not assignment_links:
                clean_name = assignment_name.replace('"', '').replace("'", '')
                self.logger.info(f"Trying without quotes: '{clean_name}'")
                assignment_links = self.driver.find_elements(By.XPATH, f"//a[contains(text(), '{clean_name}')]")
                
                # Also try matching with emojis removed from both sides
                if not assignment_links:
                    clean_name_no_emoji = self._remove_emojis(clean_name)
                    all_links = self.driver.find_elements(By.XPATH, "//td[contains(@class, 'd_dg_col_Name')]//a")
                    for link in all_links:
                        try:
                            link_text = link.text.strip()
                            link_text_no_emoji = self._remove_emojis(link_text)
                            # Normalize: dashes to spaces, comma spacing, collapse spaces
                            clean_normalized = re.sub(r'[-–—−]', ' ', clean_name_no_emoji)
                            clean_normalized = re.sub(r',\s*', ', ', clean_normalized)
                            clean_normalized = re.sub(r'\s+', ' ', clean_normalized).strip().lower()
                            link_normalized = re.sub(r'[-–—−]', ' ', link_text_no_emoji)
                            link_normalized = re.sub(r',\s*', ', ', link_normalized)
                            link_normalized = re.sub(r'\s+', ' ', link_normalized).strip().lower()
                            # EXACT MATCH ONLY after normalization
                            if clean_normalized == link_normalized:
                                self.logger.info(f"SUCCESS: Found exact normalized match! '{link_text}'")
                                assignment_links = [link]
                                break
                        except:
                            continue
            
            # If still no match, try the key part only
            if not assignment_links and 'key' in assignment_name:
                key_part = assignment_name.replace(' key', '')
                self.logger.info(f"Trying without 'key': '{key_part}'")
                assignment_links = self.driver.find_elements(By.XPATH, f"//a[contains(text(), '{key_part}')]")
                
                # Also try with emojis removed
                if not assignment_links:
                    key_part_no_emoji = self._remove_emojis(key_part)
                    all_links = self.driver.find_elements(By.XPATH, "//td[contains(@class, 'd_dg_col_Name')]//a")
                    for link in all_links:
                        try:
                            link_text = link.text.strip()
                            link_text_no_emoji = self._remove_emojis(link_text)
                            if key_part_no_emoji.lower() in link_text_no_emoji.lower() or link_text_no_emoji.lower() in key_part_no_emoji.lower():
                                self.logger.info(f"SUCCESS: Found match ignoring emojis! '{link_text}'")
                                assignment_links = [link]
                                break
                        except:
                            continue
            
            if assignment_links:
                self.logger.info(f"EXACT MATCH: Found {len(assignment_links)} assignment name links")
                for i, link in enumerate(assignment_links):
                    self.logger.info(f"  Exact match {i+1}: '{link.text.strip()}'")
            else:
                # Strategy 2: Show what we actually found for debugging
                self.logger.error(f"NO EXACT MATCHES FOUND for '{assignment_name}'")
                self.logger.error("Available assignment names on page:")
                
                # Show all assignment-like links for debugging
                all_assignment_links = self.driver.find_elements(By.XPATH, "//td[contains(@class, 'd_dg_col_Name')]//a")
                for i, link in enumerate(all_assignment_links[:10]):
                    try:
                        text = link.text.strip()
                        if text and len(text) > 5:
                            self.logger.error(f"  Available {i+1}: '{text}'")
                    except:
                        continue
            
            if assignment_links:
                self.logger.info(f"Found {len(assignment_links)} assignment name links")
                assignment_link = assignment_links[0]
                
                # Find the parent row (tr) of this assignment
                parent_row = assignment_link.find_element(By.XPATH, "./ancestor::tr")
                self.logger.info("Found parent row for the assignment")
                
                # Look for due date links within this row - UPDATED TO HANDLE DASHES
                due_date_links = parent_row.find_elements(By.XPATH, ".//a[@title='Edit the due date']")
                if not due_date_links:
                    # Try finding links in the due date column specifically
                    due_date_cells = parent_row.find_elements(By.XPATH, ".//td[contains(@class, 'd_dg_col_DueDate')]")
                    for cell in due_date_cells:
                        cell_links = cell.find_elements(By.XPATH, ".//a")
                        for link in cell_links:
                            link_text = link.text.strip()
                            # Accept both actual dates AND dashes (empty date fields)
                            if (any(pattern in link_text for pattern in ['2025', '2026', '/', 'PM', 'AM']) or 
                                link_text == '-' or link_text == ''):
                                due_date_links.append(link)
                                self.logger.info(f"Found due date link (including dash): '{link_text}'")
                                break
                    
                    # Fallback: try alternative selectors within the row
                    if not due_date_links:
                        due_date_links = parent_row.find_elements(By.XPATH, ".//a[contains(@class, 'd2l-link-inline')]")
                        # Filter for date-like text OR dashes
                        date_links = []
                        for link in due_date_links:
                            link_text = link.text.strip()
                            if (any(pattern in link_text for pattern in ['2025', '2026', '/', 'PM', 'AM']) or 
                                link_text == '-'):
                                date_links.append(link)
                        due_date_links = date_links
                
                if due_date_links:
                    self.logger.info(f"Found due date link in the same row")
                    return due_date_links[0]
                else:
                    self.logger.info("No due date link found in the assignment row")
            
            # Strategy 2: If that doesn't work, try finding by table structure
            assignment_cells = self.driver.find_elements(By.XPATH, f"//td[contains(., '{assignment_name}')]")
            
            if assignment_cells:
                self.logger.info(f"Found {len(assignment_cells)} cells containing assignment name")
                
                for assignment_cell in assignment_cells:
                    try:
                        # Find the parent row
                        parent_row = assignment_cell.find_element(By.XPATH, "./ancestor::tr")
                        
                        # Look for due date links within this row
                        due_date_links = parent_row.find_elements(By.XPATH, ".//a[@title='Edit the due date']")
                        if not due_date_links:
                            due_date_links = parent_row.find_elements(By.XPATH, ".//a[contains(@class, 'd2l-link-inline')]")
                            # Filter for date-like text
                            date_links = []
                            for link in due_date_links:
                                link_text = link.text.strip()
                                if any(pattern in link_text for pattern in ['2025', '2026', '/', 'PM', 'AM']):
                                    date_links.append(link)
                            due_date_links = date_links
                        
                        if due_date_links:
                            due_date_text = due_date_links[0].text.strip()
                            self.logger.info(f"Found due date link: '{due_date_text}'")
                            return due_date_links[0]
                    except Exception as e:
                        self.logger.info(f"Could not process assignment cell: {e}")
                        continue
            
            self.logger.error(f"Could not find due date link for assignment: '{assignment_name}'")
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding assignment due date link: {e}")
            return None
    
    def find_assignment_start_date_link(self, assignment_name):
        """Find the start date link for a specific assignment by name with fuzzy matching"""
        try:
            self.logger.info(f"Looking for start date link for assignment: '{assignment_name}'")
            
            # Strategy 1: Exact match - try multiple variations
            self.logger.info(f"Searching for EXACT match: '{assignment_name}'")
            
            # Try exact match first
            assignment_links = self.driver.find_elements(By.XPATH, f"//a[contains(text(), '{assignment_name}')]")
            if assignment_links:
                self.logger.info(f"SUCCESS: Found exact match!")
            
            # If no exact match, try normalized matching (remove dashes, normalize commas, remove emojis)
            if not assignment_links:
                # Normalize search term: remove dashes, normalize comma spacing, collapse spaces
                import re
                name_normalized = re.sub(r'[-–—−]', ' ', assignment_name)  # Replace dashes with spaces
                name_normalized = re.sub(r',\s*', ', ', name_normalized)  # Normalize comma spacing to ", "
                name_normalized = re.sub(r'\s+', ' ', name_normalized).strip()  # Collapse multiple spaces
                name_normalized = self._remove_emojis(name_normalized)  # Remove emojis
                name_normalized_lower = name_normalized.lower()
                self.logger.info(f"Trying normalized search: '{name_normalized}'")
                
                # Find all links and check their text with the same normalization
                all_links = self.driver.find_elements(By.XPATH, "//td[contains(@class, 'd_dg_col_Name')]//a")
                for link in all_links:
                    try:
                        link_text = link.text.strip()
                        link_normalized = re.sub(r'[-–—−]', ' ', link_text)  # Replace dashes with spaces
                        link_normalized = re.sub(r',\s*', ', ', link_normalized)  # Normalize comma spacing to ", "
                        link_normalized = re.sub(r'\s+', ' ', link_normalized).strip()  # Collapse multiple spaces
                        link_normalized = self._remove_emojis(link_normalized)  # Remove emojis
                        link_normalized_lower = link_normalized.lower()
                        
                        # EXACT MATCH ONLY after normalization - prevents confusion between similar assignments
                        if name_normalized_lower == link_normalized_lower:
                            self.logger.info(f"SUCCESS: Found exact normalized match! '{link_text}'")
                            assignment_links = [link]
                            break
                    except:
                        continue
            
            # If still no match, try without quotes and emojis
            if not assignment_links:
                clean_name = assignment_name.replace('"', '').replace("'", '')
                self.logger.info(f"Trying without quotes: '{clean_name}'")
                assignment_links = self.driver.find_elements(By.XPATH, f"//a[contains(text(), '{clean_name}')]")
                
                # Also try matching with emojis removed from both sides
                if not assignment_links:
                    clean_name_no_emoji = self._remove_emojis(clean_name)
                    all_links = self.driver.find_elements(By.XPATH, "//td[contains(@class, 'd_dg_col_Name')]//a")
                    for link in all_links:
                        try:
                            link_text = link.text.strip()
                            link_text_no_emoji = self._remove_emojis(link_text)
                            # Normalize: dashes to spaces, comma spacing, collapse spaces
                            clean_normalized = re.sub(r'[-–—−]', ' ', clean_name_no_emoji)
                            clean_normalized = re.sub(r',\s*', ', ', clean_normalized)
                            clean_normalized = re.sub(r'\s+', ' ', clean_normalized).strip().lower()
                            link_normalized = re.sub(r'[-–—−]', ' ', link_text_no_emoji)
                            link_normalized = re.sub(r',\s*', ', ', link_normalized)
                            link_normalized = re.sub(r'\s+', ' ', link_normalized).strip().lower()
                            # EXACT MATCH ONLY after normalization
                            if clean_normalized == link_normalized:
                                self.logger.info(f"SUCCESS: Found exact normalized match! '{link_text}'")
                                assignment_links = [link]
                                break
                        except:
                            continue
                if assignment_links:
                    self.logger.info(f"SUCCESS: Found match without quotes!")
            
            # If still no match, try the key part only
            if not assignment_links and 'key' in assignment_name:
                key_part = assignment_name.replace(' key', '')
                self.logger.info(f"Trying without 'key': '{key_part}'")
                assignment_links = self.driver.find_elements(By.XPATH, f"//a[contains(text(), '{key_part}')]")
                
                # Also try with emojis removed
                if not assignment_links:
                    key_part_no_emoji = self._remove_emojis(key_part)
                    all_links = self.driver.find_elements(By.XPATH, "//td[contains(@class, 'd_dg_col_Name')]//a")
                    for link in all_links:
                        try:
                            link_text = link.text.strip()
                            link_text_no_emoji = self._remove_emojis(link_text)
                            if key_part_no_emoji.lower() in link_text_no_emoji.lower() or link_text_no_emoji.lower() in key_part_no_emoji.lower():
                                self.logger.info(f"SUCCESS: Found match ignoring emojis! '{link_text}'")
                                assignment_links = [link]
                                break
                        except:
                            continue
                if assignment_links:
                    self.logger.info(f"SUCCESS: Found match without 'key'!")
            
            if not assignment_links:
                # Strategy 2: Show what we actually found for debugging
                self.logger.error(f"NO EXACT MATCHES FOUND for '{assignment_name}'")
                self.logger.error("Available content names on page:")
                
                # Show all content including content topics
                all_content_links = self.driver.find_elements(By.XPATH, "//td[contains(@class, 'd_dg_col_Name')]//a")
                self.logger.error(f"Found {len(all_content_links)} total content items:")
                # Show first 15
                for i, link in enumerate(all_content_links[:15]):
                    try:
                        text = link.text.strip()
                        if text and len(text) > 2:
                            self.logger.error(f"  Available {i+1}: '{text}'")
                    except:
                        continue
            
            if assignment_links:
                self.logger.info(f"Found {len(assignment_links)} assignment name links")
                assignment_link = assignment_links[0]
                
                # Find the parent row (tr) of this assignment
                parent_row = assignment_link.find_element(By.XPATH, "./ancestor::tr")
                self.logger.info("Found parent row for the assignment")
                
                # Use EXACT selectors from user recording
                start_date_selectors = [
                    ".//td[contains(@class, 'd_dg_col_StartDate')]//a",  # Exact from recording
                    ".//td[contains(@class, 'StartDate')]//a",  # Fallback
                    ".//a[@title='Edit the start date']",  # Standard pattern
                ]
                
                for selector in start_date_selectors:
                    try:
                        start_date_links = parent_row.find_elements(By.XPATH, selector)
                        if start_date_links:
                            # Filter for date-like text (including "-" which means create new date)
                            for link in start_date_links:
                                link_text = link.text.strip()
                                if link_text == '-':
                                    self.logger.info(f"Found clickable '-' link to create new start date")
                                    return link
                                if any(pattern in link_text for pattern in ['2025', '2026', '/', 'PM', 'AM', 'No start date']):
                                    self.logger.info(f"Found start date link with selector '{selector}': '{link_text}'")
                                    return link
                    except Exception as e:
                        continue
                
                # Fallback: Look for any links in the row that might be start dates
                all_links = parent_row.find_elements(By.XPATH, ".//a[contains(@class, 'd2l-link-inline')]")
                self.logger.info(f"Found {len(all_links)} total links in assignment row")
                
                for i, link in enumerate(all_links):
                    link_text = link.text.strip()
                    href = link.get_attribute('href') or ''
                    
                    # Look for start date patterns (different from due date)
                    if ('start' in href.lower() or 
                        'availability' in href.lower() or
                        link_text == 'No start date' or
                        (any(pattern in link_text for pattern in ['2025', '2026', '/', 'PM', 'AM']) and 
                         'due' not in href.lower())):  # Exclude due date links
                        self.logger.info(f"Potential start date link found: '{link_text}'")
                        return link
            
            # Strategy 2: Look for table cells that contain the assignment name
            assignment_cells = self.driver.find_elements(By.XPATH, f"//td[contains(., '{assignment_name}')]")
            
            if assignment_cells:
                self.logger.info(f"Found {len(assignment_cells)} cells containing assignment name")
                
                for assignment_cell in assignment_cells:
                    try:
                        # Find the parent row
                        parent_row = assignment_cell.find_element(By.XPATH, "./ancestor::tr")
                        
                        # Look for start date column specifically
                        start_date_cells = parent_row.find_elements(By.XPATH, ".//td[contains(@class, 'd_dg_col_StartDate') or contains(@class, 'StartDate') or contains(@headers, 'StartDate')]")
                        
                        for cell in start_date_cells:
                            start_links = cell.find_elements(By.XPATH, ".//a")
                            for link in start_links:
                                link_text = link.text.strip()
                                # Accept both actual dates AND dashes (empty date fields)
                                if (any(pattern in link_text for pattern in ['2025', '2026', '/', 'PM', 'AM']) or 
                                    link_text == '-' or link_text == ''):
                                    self.logger.info(f"Found start date link (including dash): '{link_text}'")
                                    return link
                    except Exception as e:
                        self.logger.info(f"Could not process assignment cell: {e}")
                        continue
            
            self.logger.error(f"Could not find start date link for assignment: '{assignment_name}'")
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding assignment start date link: {e}")
            return None
    
    def set_date_in_mini_editor(self, new_date, new_time):
        """Set date and time in the mini editor popup"""
        try:
            self.logger.info(f"Setting date to '{new_date}' and time to '{new_time}' in mini editor...")
            
            # Wait for dialog to appear
            wait = WebDriverWait(self.driver, 10)
            dialog = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='dialog']")))
            self.logger.info("SUCCESS: Dialog appeared")
            
            # Find all iframes within the dialog
            iframes = dialog.find_elements(By.TAG_NAME, "iframe")
            self.logger.info(f"Found {len(iframes)} iframe(s) in dialog")
            
            if not iframes:
                self.logger.error("No iframes found in dialog")
                return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0}
            
            # Try each iframe to find the one with date fields
            for i, iframe in enumerate(iframes):
                self.logger.info(f"Switching to iframe {i}...")
                self.driver.switch_to.frame(iframe)
                
                # Check if this iframe contains date fields using JavaScript
                has_date_fields = self.driver.execute_script("""
                    var dateFields = document.querySelectorAll('input[name*="year"], input[name*="month"], input[name*="day"]');
                    return dateFields.length > 0;
                """)
                
                if has_date_fields:
                    self.logger.info(f"Found date fields in iframe {i}!")
                    break
                else:
                    self.logger.info(f"No date fields in iframe {i}, trying next...")
                    self.driver.switch_to.default_content()
            else:
                self.logger.error("No iframe with date fields found")
                self.driver.switch_to.default_content()
                return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0}
            
            # Now we're in the correct iframe - set the date
            return self.set_date_in_iframe(new_date, new_time)
        
        except Exception as e:
            self.logger.error(f"Error setting date in mini editor: {e}")
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0}
    
    def set_start_date_in_mini_editor(self, new_date, new_time):
        """Set start date in mini editor - handles start date checkbox"""
        try:
            self.logger.info(f"Setting start date to '{new_date}' and time to '{new_time}' in mini editor...")
            
            # Wait for dialog to appear
            self.logger.info("Waiting for start date dialog to appear...")
            dialog_found = False
            
            # Try multiple dialog selectors
            dialog_selectors = [
                (By.CSS_SELECTOR, "[role='dialog']"),
                (By.TAG_NAME, "iframe"),
                (By.CLASS_NAME, "d2l-dialog"),
                (By.CSS_SELECTOR, ".d2l-dialog"),
            ]
            
            for selector_type, selector_value in dialog_selectors:
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((selector_type, selector_value))
                    )
                    self.logger.info(f"SUCCESS: Dialog found with selector: {selector_type} = '{selector_value}'")
                    dialog_found = True
                    break
                except:
                    continue
            
            if not dialog_found:
                self.logger.error("FAILED: No dialog found")
                return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0}
            
            # Find all iframes in the dialog
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            self.logger.info(f"Found {len(iframes)} iframe(s) in dialog")
            
            if not iframes:
                self.logger.error("No iframes found in dialog")
                return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0}
            
            # Try each iframe to find the one with date fields
            for i, iframe in enumerate(iframes):
                self.logger.info(f"Switching to iframe {i}...")
                self.driver.switch_to.frame(iframe)
                
                # Check if this iframe contains date fields
                has_date_fields = self.driver.execute_script("""
                    var dateFields = document.querySelectorAll('input[name*="year"], input[name*="month"], input[name*="day"]');
                    return dateFields.length > 0;
                """)
                
                if has_date_fields:
                    self.logger.info(f"Found date fields in iframe {i}!")
                    break
                else:
                    self.logger.info(f"No date fields in iframe {i}, trying next...")
                    self.driver.switch_to.default_content()
            else:
                self.logger.error("No iframe with date fields found")
                self.driver.switch_to.default_content()
                return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0}
            
            # Now we're in the correct iframe - set the start date with start date checkbox
            return self.set_date_in_iframe(new_date, new_time, checkbox_id="z_o")
        
        except Exception as e:
            self.logger.error(f"Error setting start date in mini editor: {e}")
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0}
    
    def set_date_in_iframe(self, new_date, new_time, checkbox_id=None):
        """Set date and time in the iframe"""
        try:
            self.logger.info(f"Setting date to '{new_date}' and time to '{new_time}' inside iframe...")
            
            # Parse the date and time
            try:
                if '/' in new_date:
                    month, day, year = new_date.split('/')
                else:
                    from datetime import datetime
                    dt = datetime.strptime(new_date, '%B %d, %Y')
                    month, day, year = str(dt.month), str(dt.day), str(dt.year)
                
                # Parse time
                if 'PM' in new_time.upper():
                    time_part = new_time.upper().replace('PM', '').strip()
                    if ':' in time_part:
                        hour, minute = time_part.split(':')
                    else:
                        hour, minute = time_part, '0'
                    hour = str(int(hour) + 12 if int(hour) != 12 else 12)
                elif 'AM' in new_time.upper():
                    time_part = new_time.upper().replace('AM', '').strip()
                    if ':' in time_part:
                        hour, minute = time_part.split(':')
                    else:
                        hour, minute = time_part, '0'
                    hour = str(int(hour) if int(hour) != 12 else 0)
                else:
                    if ':' in new_time:
                        hour, minute = new_time.split(':')
                    else:
                        hour, minute = new_time, '0'
                
                self.logger.info(f"Parsed date: {month}/{day}/{year}, time: {hour}:{minute}")
                
            except Exception as e:
                self.logger.error(f"Error parsing date/time: {e}")
                return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0}
            
            # STEP 1: Check appropriate checkbox
            checkbox_result = {'found': False, 'wasUnchecked': False, 'nowChecked': False}
            
            if checkbox_id:
                checkbox_selector = checkbox_id
                checkbox_name = "Has Start Date" if checkbox_id == "z_o" else "Has Due Date"
            else:
                checkbox_selector = "z_k"
                checkbox_name = "Has Due Date"
            
            try:
                self.logger.info(f"Looking for '{checkbox_name}' checkbox (#{checkbox_selector})")
                checkbox = self.driver.find_element(By.ID, checkbox_selector)
                checkbox_result['found'] = True
                
                is_checked = checkbox.is_selected()
                if is_checked:
                    self.logger.info(f"Checkbox is already checked")
                    checkbox_result['nowChecked'] = True
                else:
                    self.logger.info(f"Clicking checkbox to enable date fields...")
                    checkbox_result['wasUnchecked'] = True
                    
                    if checkbox_id == "z_o":
                        # Start date checkbox - use D2L event system
                        try:
                            self.driver.execute_script("""
                                var checkbox = arguments[0];
                                checkbox.checked = true;
                                checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                                checkbox.dispatchEvent(new Event('input', { bubbles: true }));
                            """, checkbox)
                            time.sleep(0.2)
                            
                            if checkbox.is_selected():
                                self.logger.info("Checkbox activated successfully!")
                                checkbox_result['nowChecked'] = True
                            else:
                                self.logger.error("Checkbox activation failed")
                                checkbox_result['nowChecked'] = False
                        except Exception as e:
                            self.logger.error(f"Checkbox click error: {e}")
                            checkbox_result['nowChecked'] = False
                    else:
                        # Due date checkbox - standard click
                        try:
                            checkbox.click()
                            time.sleep(0.2)
                            
                            if checkbox.is_selected():
                                self.logger.info("Checkbox clicked successfully!")
                                checkbox_result['nowChecked'] = True
                            else:
                                self.logger.error("Checkbox click failed")
                                checkbox_result['nowChecked'] = False
                        except Exception as e:
                            self.logger.error(f"Checkbox click error: {e}")
                            checkbox_result['nowChecked'] = False
                            
            except Exception as e:
                self.logger.error(f"Checkbox not found: {e}")
                checkbox_result['found'] = False
                return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0, 'checkboxResult': checkbox_result}
            
            # If checkbox was required but not checked, abort
            if checkbox_id and not checkbox_result.get('nowChecked', False):
                self.logger.error("Checkbox activation failed - cannot proceed")
                return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0, 'checkboxResult': checkbox_result}
            
            # STEP 2: Set date/time
            result = self.driver.execute_script("""
                const month = arguments[0];
                const day = arguments[1]; 
                const year = arguments[2];
                const hour = arguments[3];
                const minute = arguments[4];
                
                const yearField = document.querySelector('input[name*="$year"]');
                const monthField = document.querySelector('input[name*="$month"]');  
                const dayField = document.querySelector('input[name*="$day"]');
                const hourField = document.querySelector('input[name*="$hour"]');
                const minuteField = document.querySelector('input[name*="$minute"]');
                
                let dateFound = false;
                let dateSet = false;
                let timeFound = false;
                let timeSet = false;
                
                if (yearField && monthField && dayField) {
                    dateFound = true;
                    try {
                        yearField.value = year;
                        monthField.value = month;
                        dayField.value = day;
                        
                        [yearField, monthField, dayField].forEach(field => {
                            field.dispatchEvent(new Event('input', { bubbles: true }));
                            field.dispatchEvent(new Event('change', { bubbles: true }));
                        });
                        
                        dateSet = true;
                    } catch (e) {
                        console.error('Error setting date:', e);
                    }
                }
                
                if (hourField && minuteField) {
                    timeFound = true;
                    try {
                        hourField.value = hour;
                        minuteField.value = minute;
                        
                        [hourField, minuteField].forEach(field => {
                            field.dispatchEvent(new Event('input', { bubbles: true }));
                            field.dispatchEvent(new Event('change', { bubbles: true }));
                        });
                        
                        timeSet = true;
                    } catch (e) {
                        console.error('Error setting time:', e);
                    }
                }
                
                return {
                    dateFound: dateFound,
                    dateSet: dateSet,
                    timeFound: timeFound,
                    timeSet: timeSet,
                    totalElements: (yearField ? 1 : 0) + (monthField ? 1 : 0) + (dayField ? 1 : 0) + (hourField ? 1 : 0) + (minuteField ? 1 : 0)
                };
            """, month, day, year, hour, minute)
            
            result['checkboxResult'] = checkbox_result
            
            if result['dateSet']:
                self.logger.info(f"Successfully set date to {month}/{day}/{year}")
            if result['timeSet']:
                self.logger.info(f"Successfully set time to {hour}:{minute}")
            
            # STEP 3: Click Save button
            try:
                self.driver.switch_to.default_content()
                
                save_selectors = [
                    "//button[text()='Save']",
                    "//div[@class='ddial_o']//button[1]",
                    "//button[contains(text(), 'Save')]",
                ]
                
                save_clicked = False
                for selector in save_selectors:
                    try:
                        save_button = self.driver.find_element(By.XPATH, selector)
                        if save_button.is_displayed() and save_button.is_enabled():
                            save_button.click()
                            self.logger.info("Clicked Save button")
                            save_clicked = True
                            break
                    except:
                        continue
                
                result['saveClicked'] = save_clicked
                time.sleep(0.5)
                    
            except Exception as e:
                self.logger.warning(f"Error clicking Save: {e}")
                result['saveClicked'] = False
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in set_date_in_iframe: {e}")
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return {'dateFound': False, 'dateSet': False, 'timeFound': False, 'timeSet': False, 'totalElements': 0}


class D2LDateProcessorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D2L Date Processor - Bulk Date Editor")
        self.root.geometry("700x600")
        
        self.automation = None
        self.csv_file_path = None
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the GUI widgets"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # URL selection
        ttk.Label(main_frame, text="D2L Course URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.url_var = tk.StringVar(value="https://d2l.lonestar.edu/d2l/home/1567310")
        url_frame = ttk.Frame(main_frame)
        url_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        url_frame.columnconfigure(0, weight=1)
        
        self.url_combo = ttk.Combobox(url_frame, textvariable=self.url_var, width=50)
        self.url_combo['values'] = (
            "https://d2l.lonestar.edu/d2l/home/1567310",
            "https://d2l.lonestar.edu/d2l/home/1567309"
        )
        self.url_combo.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # CSV file selection
        csv_frame = ttk.LabelFrame(main_frame, text="CSV File", padding="5")
        csv_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        csv_frame.columnconfigure(1, weight=1)
        
        ttk.Label(csv_frame, text="CSV File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.csv_var = tk.StringVar(value="No file selected")
        self.csv_label = ttk.Label(csv_frame, textvariable=self.csv_var, foreground="gray")
        self.csv_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        self.browse_button = ttk.Button(csv_frame, text="Browse...", command=self.browse_csv_file)
        self.browse_button.grid(row=0, column=2, padx=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.login_button = ttk.Button(button_frame, text="Login to D2L", command=self.login_to_d2l)
        self.login_button.grid(row=0, column=0, padx=5)
        
        self.process_button = ttk.Button(button_frame, text="Process CSV", command=self.process_csv, state=tk.DISABLED)
        self.process_button.grid(row=0, column=1, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear Login", command=self.clear_login)
        self.clear_button.grid(row=0, column=2, padx=5)
        
        self.exit_button = ttk.Button(button_frame, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=0, column=3, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)
        
        self.status_var = tk.StringVar(value="Ready - Select CSV file and click 'Login to D2L' to begin")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(status_frame, height=15, width=80)
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        main_frame.rowconfigure(4, weight=1)
    
    def browse_csv_file(self):
        """Browse for CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            self.csv_file_path = file_path
            self.csv_var.set(os.path.basename(file_path))
            self.csv_label.config(foreground="black")
            self.update_status(f"Selected CSV file: {os.path.basename(file_path)}")
        
    def update_status(self, message):
        """Update the status label and log"""
        self.status_var.set(message)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def login_to_d2l(self):
        """Handle login process"""
        try:
            self.update_status("Initializing Chrome driver...")
            
            if not hasattr(self, 'automation') or self.automation is None:
                self.automation = D2LDateProcessor()
            
            if not self.automation.setup_driver():
                self.update_status("Failed to initialize driver")
                return
            
            d2l_url = self.url_var.get()
            self.update_status(f"Navigating to: {d2l_url}")
            self.automation.driver.get(d2l_url)
            time.sleep(2)
            
            self.update_status("Login successful! Navigate to 'Manage Dates' page")
            self.process_button.config(state=tk.NORMAL)
            self.update_status("Ready for CSV processing!")
                
        except Exception as e:
            self.update_status(f"Login error: {e}")
    
    def process_csv(self):
        """Process the CSV file"""
        try:
            if not self.csv_file_path:
                messagebox.showerror("Error", "Please select a CSV file first")
                return
            
            if not self.automation or not self.automation.driver:
                messagebox.showerror("Error", "Please login to D2L first")
                return
            
            self.update_status("Starting CSV processing...")
            
            processed, errors = self.automation.process_csv_file(self.csv_file_path)
            
            if errors == 0:
                self.update_status(f"Success! Processed {processed} assignments")
                messagebox.showinfo("Success", f"Successfully processed {processed} assignments!")
            else:
                self.update_status(f"Completed: {processed} processed, {errors} errors")
                messagebox.showwarning("Completed with Errors", f"Processed {processed}, but {errors} had errors.")
                
        except Exception as e:
            self.update_status(f"CSV processing error: {e}")
            messagebox.showerror("Error", f"CSV processing failed: {e}")
    
    def clear_login(self):
        """Clear saved login session"""
        try:
            self.update_status("Clearing login session...")
            
            if hasattr(self, 'automation') and self.automation and self.automation.driver:
                self.automation.driver.quit()
                self.automation = None
            
            import tempfile
            profile_dir = os.path.join(tempfile.gettempdir(), "d2l_chrome_profile")
            if os.path.exists(profile_dir):
                shutil.rmtree(profile_dir)
                self.update_status("Login session cleared!")
            else:
                self.update_status("No saved session found")
            
            self.process_button.config(state=tk.DISABLED)
            
        except Exception as e:
            self.update_status(f"Error clearing login: {e}")
    
    def exit_app(self):
        """Exit the application"""
        try:
            if hasattr(self, 'automation') and self.automation and self.automation.driver:
                self.automation.driver.quit()
        except:
            pass
        
        self.root.destroy()
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def cleanup_existing_processes():
    """Clean up any existing Chrome/ChromeDriver processes"""
    try:
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] in ['chrome.exe', 'chromedriver.exe']:
                    proc.kill()
        except ImportError:
            try:
                subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'], capture_output=True, text=True)
                subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], capture_output=True, text=True)
            except:
                pass
    except:
        pass


def main():
    """Main function"""
    print("Starting D2L Date Processor - Bulk Date Editor...")
    cleanup_existing_processes()
    print("Launching GUI...")
    
    app = D2LDateProcessorGUI()
    app.run()


if __name__ == "__main__":
    main()