#!/usr/bin/env python3
"""
D2L Date Processor - Bulk Date Assignment Editor with CSV Support
Refactored into modular components for better maintainability
"""

import time
import logging
import os
import csv
from core.browser_manager import BrowserManager
from core.assignment_finder import AssignmentFinder
from core.date_editor import DateEditor

class D2LDateProcessor:
    def __init__(self):
        self.browser_manager = BrowserManager()
        self.driver = None
        self.assignment_finder = None
        self.date_editor = None
        self.logger = self.browser_manager.logger
        
    def setup_driver(self, use_profile=True):
        """Setup Chrome driver with persistent login session"""
        success = self.browser_manager.setup_driver(use_profile)
        if success:
            self.driver = self.browser_manager.driver
            self.assignment_finder = AssignmentFinder(self.driver, self.logger)
            self.date_editor = DateEditor(self.driver, self.logger)
        return success
    
    def process_csv_file(self, csv_file_path):
        """Process CSV file and update assignments"""
        try:
            self.logger.info(f"Processing CSV file: {csv_file_path}")
            
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Validate CSV headers
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
                        
                        # Clean the assignment name of quotes
                        clean_assignment_name = assignment_name.strip('"').strip("'").strip()
                        if clean_assignment_name != assignment_name:
                            self.logger.info(f"Cleaned assignment name: '{clean_assignment_name}'")
                        
                        # Process due date FIRST (to avoid D2L validation errors)
                        start_success = False
                        due_success = False
                        
                        due_date = row['Due Date'].strip()
                        due_time = row['Due Time'].strip()
                        
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
            due_date_link = self.assignment_finder.find_assignment_due_date_link(assignment_name)
            if not due_date_link:
                return False
            
            # Click the due date link
            self.driver.execute_script("arguments[0].scrollIntoView(true);", due_date_link)
            time.sleep(0.5)
            due_date_link.click()
            self.logger.info("Clicked due date link")
            time.sleep(2)
            
            # Set the date in the mini editor
            result = self.date_editor.set_date_in_mini_editor(due_date, due_time)
            return result.get('dateSet', False) or result.get('timeSet', False)
            
        except Exception as e:
            self.logger.error(f"Error setting due date for '{assignment_name}': {e}")
            return False
    
    def set_assignment_start_date(self, assignment_name, start_date, start_time):
        """Set start date for a specific assignment"""
        try:
            # Find and click the start date link
            start_date_link = self.assignment_finder.find_assignment_start_date_link(assignment_name)
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
            result = self.date_editor.set_start_date_in_mini_editor(start_date, start_time)
            return result.get('dateSet', False) or result.get('timeSet', False)
            
        except Exception as e:
            self.logger.error(f"Error setting start date for '{assignment_name}': {e}")
            return False
    
    def close(self):
        """Close the browser"""
        if self.browser_manager:
            self.browser_manager.close()
