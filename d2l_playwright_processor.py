#!/usr/bin/env python3
"""
D2L Date Processor using Playwright - Persistent browser session (no second tab)
"""

import asyncio
import csv
import json
import os
import sys
from playwright.async_api import async_playwright

class D2LPlaywrightProcessor:
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None

    async def setup_browser(self):
        """Setup Playwright browser - persistent user session (copied from agent.py)"""
        try:
            self.playwright = await async_playwright().start()
            
            # Use shared browser data directory
            browser_data_dir = r"C:\Users\chase\Documents\Shared-Browser-Data"
            if not os.path.exists(browser_data_dir):
                os.makedirs(browser_data_dir)
                print(f"Created shared browser data directory: {browser_data_dir}")
            print("✅ Using shared browser data from:", browser_data_dir)
            
            # Launch persistent context exactly like agent.py
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=browser_data_dir,
                headless=False,
                args=['--remote-debugging-port=9223', '--window-position=100,100', '--window-size=1920,1080']
            )
            
            # Reuse existing page or create new one (exactly like agent.py)
            self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
            
            print("Browser started with persistent session")
            return True
            
        except Exception as e:
            print(f"Error setting up browser: {e}")
            return False

    async def navigate_to_class(self, class_url):
        try:
            await self.page.bring_to_front()
            current_url = self.page.url.lower()
            if class_url.lower() != current_url:
                await self.page.goto(class_url)
            await self.page.wait_for_load_state('networkidle')
            print(f"Navigated to class: {class_url}")
            return True
        except Exception as e:
            print(f"Error navigating to class: {e}")
            return False

    async def process_csv_file(self, csv_file_path):
        try:
            print(f"Processing CSV file: {csv_file_path}")
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                required_headers = ['Name', 'Start Date', 'Start Time', 'Due Date', 'Due Time']
                if not all(header in reader.fieldnames for header in required_headers):
                    raise ValueError(f"CSV must have required headers: {required_headers}")

                processed_count, error_count = 0, 0
                for row_num, row in enumerate(reader, start=2):
                    try:
                        assignment_name = row['Name'].strip()
                        if not assignment_name:
                            print(f"Row {row_num}: Empty assignment name, skipping")
                            continue

                        clean_assignment_name = assignment_name.strip('"').strip("'").strip()
                        due_date, due_time = row['Due Date'].strip(), row['Due Time'].strip()
                        start_date, start_time = row['Start Date'].strip(), row['Start Time'].strip()

                        if due_date and due_time:
                            print(f"Setting due date for '{clean_assignment_name}': {due_date} at {due_time}")
                            if await self.set_assignment_due_date(clean_assignment_name, due_date, due_time):
                                processed_count += 1
                            else:
                                error_count += 1

                        if start_date and start_time:
                            print(f"Setting start date for '{clean_assignment_name}': {start_date} at {start_time}")
                            if not await self.set_assignment_start_date(clean_assignment_name, start_date, start_time):
                                error_count += 1

                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"Error processing row {row_num}: {e}")
                        error_count += 1

                print(f"CSV processing completed: {processed_count} successful, {error_count} errors")
                return processed_count, error_count
        except Exception as e:
            print(f"Error processing CSV file: {e}")
            return 0, 1

    async def set_assignment_due_date(self, assignment_name, due_date, due_time):
        try:
            assignment_row = await self.find_assignment_row(assignment_name)
            if not assignment_row:
                print(f"Could not find assignment: {assignment_name}")
                return False

            due_date_link = await assignment_row.locator("a[title='Edit the due date']").first
            if await due_date_link.count() == 0:
                print(f"No due date link found for: {assignment_name}")
                return False

            await due_date_link.click()
            await self.page.wait_for_timeout(2000)

            return await self.set_date_in_dialog(due_date, due_time)
        except Exception as e:
            print(f"Error setting due date for '{assignment_name}': {e}")
            return False

    async def set_assignment_start_date(self, assignment_name, start_date, start_time):
        try:
            assignment_row = await self.find_assignment_row(assignment_name)
            if not assignment_row:
                print(f"Could not find assignment: {assignment_name}")
                return False

            start_date_link = await assignment_row.locator("a[title='Edit the start date']").first
            if await start_date_link.count() == 0:
                print(f"No start date link found for: {assignment_name}")
                return False

            await start_date_link.click()
            await self.page.wait_for_timeout(3000)

            return await self.set_date_in_dialog(start_date, start_time, is_start_date=True)
        except Exception as e:
            print(f"Error setting start date for '{assignment_name}': {e}")
            return False

    async def find_assignment_row(self, assignment_name):
        try:
            assignment_cell = self.page.locator(f"td:has-text('{assignment_name}')").first
            if await assignment_cell.count() > 0:
                return assignment_cell.locator("xpath=./ancestor::tr")
            return None
        except Exception as e:
            print(f"Error finding assignment row: {e}")
            return None

    async def set_date_in_dialog(self, date_str, time_str, is_start_date=False):
        try:
            await self.page.wait_for_selector("[role='dialog']", timeout=10000)
            iframe = self.page.frame_locator("iframe").first
            await iframe.wait_for()

            if is_start_date:
                checkbox = iframe.locator("#z_o")
                if await checkbox.count() > 0:
                    await checkbox.check()
                    await self.page.wait_for_timeout(500)

            month, day, year = self.parse_date(date_str)
            hour, minute = self.parse_time(time_str)

            await iframe.locator('input[name*="$year"]').fill(year)
            await iframe.locator('input[name*="$month"]').fill(month)
            await iframe.locator('input[name*="$day"]').fill(day)
            await iframe.locator('input[name*="$hour"]').fill(hour)
            await iframe.locator('input[name*="$minute"]').fill(minute)

            save_button = self.page.locator("button:has-text('Save')").first
            await save_button.click()
            await self.page.wait_for_timeout(1000)
            return True
        except Exception as e:
            print(f"Error setting date in dialog: {e}")
            return False

    def parse_date(self, date_str):
        if '/' in date_str:
            month, day, year = date_str.split('/')
        else:
            from datetime import datetime
            dt = datetime.strptime(date_str, '%B %d, %Y')
            month, day, year = str(dt.month), str(dt.day), str(dt.year)
        return month, day, year

    def parse_time(self, time_str):
        if 'PM' in time_str.upper():
            time_part = time_str.upper().replace('PM', '').strip()
            hour, minute = time_part.split(':') if ':' in time_part else (time_part, '0')
            hour = str(int(hour) + 12 if int(hour) != 12 else 12)
        elif 'AM' in time_str.upper():
            time_part = time_str.upper().replace('AM', '').strip()
            hour, minute = time_part.split(':') if ':' in time_part else (time_part, '0')
            hour = str(int(hour) if int(hour) != 12 else 0)
        else:
            hour, minute = time_str.split(':') if ':' in time_str else (time_str, '0')
        return hour, minute

    async def close(self):
        try:
            if self.context:
                await self.context.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"Error closing browser: {e}")

async def main():
    if len(sys.argv) < 3:
        print(json.dumps({"success": False, "error": "Usage: python d2l_playwright_processor.py <command> <url_or_csv>"}))
        sys.exit(1)

    command = sys.argv[1]
    url_or_csv = sys.argv[2]

    processor = D2LPlaywrightProcessor()
    try:
        if not await processor.setup_browser():
            print(json.dumps({"success": False, "error": "Failed to setup browser"}))
            sys.exit(1)

        if command == "login":
            # Just open browser and navigate to URL for manual login
            await processor.page.goto(url_or_csv)
            await processor.page.wait_for_load_state('networkidle')
            print(json.dumps({"success": True, "message": "Browser opened for login"}))
            
            # Don't close browser - let it stay open
            # The browser will stay open even after this script exits
            
        elif command == "navigate":
            # Navigate to class URL in existing browser
            await processor.page.goto(url_or_csv)
            await processor.page.wait_for_load_state('networkidle')
            print(json.dumps({"success": True, "message": "Navigated to class"}))
            
            # Don't close browser - let it stay open
            
        elif command == "process":
            # Process CSV file
            if not await processor.navigate_to_class(url_or_csv):
                print(json.dumps({"success": False, "error": "Failed to navigate to class"}))
                sys.exit(1)
            
            # Get CSV file path from 3rd argument
            if len(sys.argv) < 4:
                print(json.dumps({"success": False, "error": "CSV file path required for process command"}))
                sys.exit(1)
            
            csv_file_path = sys.argv[3]
            processed, errors = await processor.process_csv_file(csv_file_path)
            print(json.dumps({"success": True, "processed": processed, "errors": errors, "message": f"Processed {processed} assignments with {errors} errors"}))
        else:
            print(json.dumps({"success": False, "error": "Unknown command. Use 'login', 'navigate', or 'process'"}))
            sys.exit(1)

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
    finally:
        # For login and navigate, don't close anything - keep browser open (like agent.py)
        if command not in ["login", "navigate"]:
            await processor.close()
        # For login and navigate commands, do NOTHING - let browser stay open

if __name__ == "__main__":
    asyncio.run(main())
