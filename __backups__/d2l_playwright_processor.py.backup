#!/usr/bin/env python3
"""
D2L Playwright Processor (Fixed to match Automation Agent behavior)
------------------------------------------------------------------
- Connects ONLY to the Chrome instance launched by Node.
- Does NOT start its own Chromium (avoids blue icon & file locks).
- Keeps session persistent using Shared-Browser-Data.
- Provides clear logging if Chrome is not running.

This version adds a new ``process`` action to facilitate schedule
processing. When invoked with ``process``, the script will open the
specified course (either by code or full URL), log the CSV path for
future automation, and return a JSON result to the caller. Full CSV
processing is not yet implemented, but the scaffolding is in place to
add that logic without disrupting existing features.
"""

import sys
import os
import json
import asyncio
import logging
import traceback
import subprocess
from datetime import datetime
from playwright.async_api import async_playwright

# ========================================
# 🔧 CONFIGURATION
# ========================================
SHARED_BROWSER_DIR = r"C:\Users\chase\Documents\Shared-Browser-Data"
D2L_BASE_URL = "https://d2l.lonestar.edu/"

COURSE_URLS = {
    "FM4202": "https://d2l.lonestar.edu/d2l/lms/manageDates/date_manager.d2l?fromCMC=1&ou=1580392",
    "FM4103": "https://d2l.lonestar.edu/d2l/lms/manageDates/date_manager.d2l?fromCMC=1&ou=1580390",
    "CA4203": "https://d2l.lonestar.edu/d2l/lms/manageDates/date_manager.d2l?fromCMC=1&ou=1580436",
    "CA4201": "https://d2l.lonestar.edu/d2l/lms/manageDates/date_manager.d2l?fromCMC=1&ou=1580434",
    "CA4105": "https://d2l.lonestar.edu/d2l/lms/manageDates/date_manager.d2l?fromCMC=1&ou=1580431",
}

# Centralized logs folder
LOGS_DIR = r"C:\Users\chase\Documents\School Scrips\Logs"
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOGS_DIR, "d2l_processor.log")
# Configure logging to write to both a file and stdout.  By default
# logging.StreamHandler writes to stderr, which may not be captured by the
# Node backend.  Explicitly direct the stream to sys.stdout to ensure
# logs are printed on stdout and thus captured by the parent process.
# Configure logging with force=True to ensure our handlers are
# registered even if another module (such as one imported by the
# Playwright library) has already configured the root logger.  The
# ``force`` parameter, added in Python 3.8+, will remove any existing
# handlers and reset the configuration.  This prevents duplicate logs
# or missing handlers when the script is run multiple times in the same
# process.  We direct log output to both a file and to stdout so that
# any supervising process (e.g. the Node backend) can capture the
# messages.  Without ``force=True`` the configuration may silently
# fail if logging has already been set up elsewhere.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ],
    force=True
)
logger = logging.getLogger(__name__)


class D2LProcessor:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        # Track how many assignments were logged/processed in a run
        self.assignments_processed = 0

    async def automate_d2l(self, action=None, course_code=None, csv_path=None):
        """
        Main coroutine that attaches to an existing Chrome instance and performs
        automation based on the provided action. Supported actions:

        - ``login`` (default): navigate to the D2L home page and hold for manual login.
        - ``open-course``: open the manage dates page for the given course code. The
          ``course_code`` may be a short code (e.g. ``CA4105``) or a full URL. If a
          short code is provided, it will be looked up in ``COURSE_URLS``. If it is
          already a URL, it will be used directly.
        - ``process``: open the manage dates page for the given course and prepare
          to process a CSV. The CSV processing itself is not implemented yet, but
          this action ensures the page is open and reports success back to the
          caller. An optional ``csv_path`` may be provided as a third CLI
          argument. The path is logged for future use.

        Parameters
        ----------
        action : str, optional
            The action to perform (``login``, ``open-course``, ``process``). Default
            is ``login``.
        course_code : str, optional
            Either a class code defined in ``COURSE_URLS`` or a direct URL to
            the manage dates page. Required for ``open-course`` and ``process``.
        csv_path : str, optional
            Path to a CSV file containing schedule data. Used by the ``process``
            action. Currently the CSV is not parsed or processed, but the path is
            logged for later implementation.
        """
        try:
            logger.info("🚀 Starting D2L automation (attach-only mode)...")
            self.playwright = await async_playwright().start()

            # ===========================================================
            # 🧩 CONNECT TO EXISTING CHROME ONLY
            # ===========================================================
            await asyncio.sleep(0.5)
            try:
                logger.info("🔗 Connecting to existing Chrome session on port 9223...")
                browser = await self.playwright.chromium.connect_over_cdp("http://localhost:9223")
                self.context = browser.contexts[0]
                self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
                logger.info("✅ Attached to existing Chrome session (no relaunch).")
            except Exception as e:
                logger.error(f"❌ Could not connect to existing browser: {e}")
                raise RuntimeError("Chrome must be opened first via the Login button.")

            # ===========================================================
            # 🌐 NAVIGATION & ACTIONS
            # ===========================================================
            if action == "open-course" and course_code:
                # Skip homepage reload — directly open the course
                logger.info(f"🎯 Opening course directly: {course_code}")
                await self.open_course(course_code)
                # Hold the page open so the user can interact manually
                logger.info("🕓 Holding browser open after opening course (open-course mode).")
                await asyncio.Event().wait()
            elif action == "process" and course_code:
                # Process schedule: open course and prepare for CSV-based automation
                logger.info(f"📅 Processing schedule for course: {course_code}")
                await self.process_course(course_code, csv_path)
            else:
                # Normal login flow — go to D2L home page
                logger.info(f"🌍 Navigating to D2L base URL: {D2L_BASE_URL}")
                await self.page.goto(D2L_BASE_URL, wait_until="networkidle")
                await asyncio.sleep(3)
                logger.info("✅ Browser ready for manual login.")
                logger.info("🕓 Holding browser open indefinitely (login mode).")
                await asyncio.Event().wait()

        except Exception as e:
            self._write_debug_report("automate_d2l", e)
            raise

    async def open_course(self, course_code: str):
        """
        Navigate to a specific course page. Accepts either a course code (key in
        ``COURSE_URLS``) or a full URL. If the provided course_code is a known
        key, the corresponding URL is used; otherwise ``course_code`` itself is
        treated as a URL.
        """
        try:
            if not self.context:
                raise RuntimeError("Browser not initialized.")
            # Resolve the URL: look up in mapping or use directly if it resembles a URL
            url = COURSE_URLS.get(course_code, course_code)
            page = self.context.pages[0] if self.context.pages else await self.context.new_page()
            logger.info(f"📘 Opening course page: {url}")
            
            # Only navigate if we aren't already on the target page
            current_url = page.url
            if not current_url.startswith(url):
                await page.goto(url, wait_until='networkidle')
                await asyncio.sleep(3)
            else:
                logger.info(f"✅ Already on target page: {current_url}")
            logger.info(f"✅ Course {course_code} loaded successfully.")
        except Exception as e:
            self._write_debug_report("open_course", e)
            raise

    async def process_course(self, course_code: str, csv_path: str = None):
        """
        Open the course manage-dates page and prepare to process a CSV. The CSV
        processing logic is currently a stub; it can be extended to read the
        provided ``csv_path`` and automate date updates using Playwright. For now
        the function simply opens the course and logs the CSV path for future
        use. After navigation, it returns successfully without blocking.

        Parameters
        ----------
        course_code : str
            The course code or full URL for the manage dates page.
        csv_path : str, optional
            Path to the CSV file containing date information. Logged but
            otherwise unused in this stub implementation.
        """
        try:
            if not self.context:
                raise RuntimeError("Browser not initialized.")
            
            url = COURSE_URLS.get(course_code, course_code)
            # reuse the current page instead of opening a new one
            page = self.page if self.page else (self.context.pages[0] if self.context.pages else await self.context.new_page())
            logger.info(f"📘 Using existing page for processing: {url}")
            
            # Check if we're already on the correct page - don't reload if we don't need to
            current_url = page.url
            if not current_url.startswith(url):
                logger.info(f"🔄 Navigating to Manage Dates page: {url}")
                await page.goto(url, wait_until='domcontentloaded')
                # wait for the assignments table to load
                await page.wait_for_selector("//td[contains(@class,'d_dg_col_Name')]", timeout=20000)
            else:
                logger.info(f"✅ Already on target page: {current_url}")
                # Just wait for the table to be ready (it should already be loaded)
                await page.wait_for_selector("//td[contains(@class,'d_dg_col_Name')]", timeout=5000)
            
            # Wait for the table to be fully populated by checking if more assignments load
            logger.info("⏳ Checking for additional assignments to load...")
            previous_count = 0
            for attempt in range(6):  # Try up to 6 times
                current_links = await page.query_selector_all("//td[contains(@class,'d_dg_col_Name')]//a")
                current_count = len(current_links)
                logger.info(f"🔍 Load attempt {attempt + 1}: Found {current_count} assignment links")
                
                if current_count > previous_count:
                    previous_count = current_count
                    await asyncio.sleep(2)  # Wait 2 seconds for more to load
                else:
                    logger.info(f"✅ Table loading complete. Total assignments found: {current_count}")
                    break
            
            # Debug: Log the current page URL and check what elements are actually present
            logger.info(f"🔍 Current page URL: {page.url}")
            
            # Debug: Check if any assignment links exist
            assignment_links = await page.query_selector_all("//td[contains(@class,'d_dg_col_Name')]//a")
            logger.info(f"🔍 Found {len(assignment_links)} assignment links on page")
            
            # Debug: Log the first few assignment names found
            for i, link in enumerate(assignment_links[:3]):
                try:
                    text = await link.text_content()
                    logger.info(f"🔍 Assignment {i+1}: '{text.strip()}'")
                except:
                    logger.info(f"🔍 Assignment {i+1}: Could not get text content")
            
            logger.info(f"✅ Course page loaded. Preparing to process CSV: {csv_path}")

            # Read the CSV file and log each assignment for debugging
            assignments_processed = 0
            assignments: list[dict] = []
            if csv_path and os.path.isfile(csv_path):
                try:
                    # Attempt to use pandas if available for flexible parsing
                    try:
                        import pandas as pd  # type: ignore
                        df = pd.read_csv(csv_path)
                        logger.info(f"📄 CSV loaded: {len(df)} rows")
                        for idx, row in df.iterrows():
                            # Support both 'Assignment Name' and legacy 'Name' headers
                            assignment = str(row.get('Assignment Name') or row.get('Name') or '').strip()
                            # Standard date fields
                            start_date = str(row.get('Start Date') or row.get('Start') or '').strip()
                            due_date = str(row.get('Due Date') or row.get('Due') or '').strip()
                            end_date = str(row.get('End Date') or row.get('End') or '').strip()
                            # Time fields may be missing; try multiple headers
                            start_time = str(row.get('Start Time') or row.get('Start Time (Local)') or '').strip()
                            due_time = str(row.get('Due Time') or row.get('Due Time (Local)') or '').strip()
                            logger.info(
                                f"🔍 [Row {idx+1}] assignment='{assignment}', start='{start_date}'{f' {start_time}' if start_time else ''}, due='{due_date}'{f' {due_time}' if due_time else ''}, end='{end_date}'"
                            )
                            assignments_processed += 1
                            assignments.append({
                                'assignment': assignment,
                                'start_date': start_date,
                                'start_time': start_time,
                                'due_date': due_date,
                                'due_time': due_time,
                                'end_date': end_date
                            })
                    except ImportError:
                        # Fallback to csv module if pandas isn't available
                        import csv as csv_module
                        with open(csv_path, newline='', encoding='utf-8') as csvfile:
                            reader = csv_module.DictReader(csvfile)
                            rows = list(reader)
                        logger.info(f"📄 CSV loaded: {len(rows)} rows")
                        for idx, row in enumerate(rows):
                            assignment = (row.get('Assignment Name') or row.get('Name') or '').strip()
                            start_date = (row.get('Start Date') or row.get('Start') or '').strip()
                            due_date = (row.get('Due Date') or row.get('Due') or '').strip()
                            end_date = (row.get('End Date') or row.get('End') or '').strip()
                            start_time = (row.get('Start Time') or row.get('Start Time (Local)') or '').strip()
                            due_time = (row.get('Due Time') or row.get('Due Time (Local)') or '').strip()
                            logger.info(
                                f"🔍 [Row {idx+1}] assignment='{assignment}', start='{start_date}'{f' {start_time}' if start_time else ''}, due='{due_date}'{f' {due_time}' if due_time else ''}, end='{end_date}'"
                            )
                            assignments_processed += 1
                            assignments.append({
                                'assignment': assignment,
                                'start_date': start_date,
                                'start_time': start_time,
                                'due_date': due_date,
                                'due_time': due_time,
                                'end_date': end_date
                            })
                except Exception as csv_err:
                    logger.error(f"❌ Error reading CSV at {csv_path}: {csv_err}")
            else:
                logger.warning(f"⚠️ CSV path missing or file not found: {csv_path}")

            # If CSV rows were found and a valid page is loaded, attempt to update dates
            # for each assignment. This preserves the existing logging-only behaviour if
            # no CSV is provided or the file cannot be read.  The actual Playwright
            # automation code has been separated into helper methods to keep
            # ``process_course`` focused on high-level orchestration.  After
            # performing date updates, the number of processed assignments will
            # reflect both logging and update attempts.

            if assignments_processed > 0:
                try:
                    # Table is already loaded from the initial navigation and wait above
                    logger.info("🛠️ Beginning automated date updates for CSV assignments...")
                    await self.perform_date_updates(page, assignments)
                except Exception as update_err:
                    logger.error(f"❌ Error updating assignment dates: {update_err}")

            # Record the number of assignments processed for reporting back via CLI
            self.assignments_processed = assignments_processed
            logger.info(f"✅ CSV processing completed. Assignments logged: {assignments_processed}")
        except Exception as e:
            self._write_debug_report("process_course", e)
            raise

    def run_automation(self, action=None, course_code=None, csv_path=None):
        """
        Launch the automation coroutine and handle cleanup. The optional
        ``csv_path`` is passed through to ``automate_d2l``. Returns True on
        success and False on error.
        """
        try:
            logger.info("🧠 Starting D2L automation process...")
            asyncio.run(self.automate_d2l(action, course_code, csv_path))
            logger.info("✅ D2L Automation completed successfully.")
            return True
        except SystemExit as e:
            logger.error(f"⛔ {e}")
            return False
        except Exception as e:
            logger.error(f"❌ D2L Automation error: {str(e)}")
            return False
        finally:
            # Cleanup
            try:
                if self.context:
                    asyncio.run(self.context.close())
                    logger.info("✅ Browser context closed.")
                if self.playwright:
                    asyncio.run(self.playwright.stop())
                    logger.info("✅ Playwright stopped.")
            except Exception as cleanup_error:
                logger.warning(f"⚠️ Cleanup error: {cleanup_error}")

    def _write_debug_report(self, stage, exception):
        """
        Write detailed debug info to a file and launch Notepad to display it.
        Useful for diagnosing unexpected errors during automation.
        """
        try:
            debug_dir = os.path.join(LOGS_DIR, "debug_logs")
            os.makedirs(debug_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            debug_path = os.path.join(debug_dir, f"debug_{stage}_{timestamp}.txt")
            with open(debug_path, "w", encoding="utf-8") as f:
                f.write(f"Stage: {stage}\n")
                f.write(f"Error: {repr(exception)}\n\n")
                f.write(traceback.format_exc())
            logger.error(f"❌ Error at {stage}: {exception}")
            logger.info(f"Debug log saved at: {debug_path}")
            subprocess.Popen(['notepad.exe', debug_path], shell=True)
        except Exception as log_err:
            print(f"Failed to write debug log: {log_err}")

    def _parse_time_str(self, time_str: str):
        """
        Parse a time string from the CSV into a 24‑hour hour and minute pair.
        Supported formats include 'HH:MM', 'H:MM', 'HH:MM AM/PM', 'H AM', etc.
        If the string is empty or cannot be parsed, returns (None, None) so
        that the time fields will not be modified.

        Parameters
        ----------
        time_str : str
            The raw time string from the CSV.

        Returns
        -------
        Tuple[str|None, str|None]
            A tuple (hour, minute) in 24‑hour format, or (None, None) if
            parsing fails or the input is empty.
        """
        if not time_str:
            return None, None
        try:
            s = time_str.strip()
            import re
            # Detect AM/PM
            am_pm_match = re.search(r'(AM|PM)$', s, re.IGNORECASE)
            if am_pm_match:
                # Split off AM/PM
                am_pm = am_pm_match.group().upper()
                s = s[:-len(am_pm)].strip()
                # Extract hour and minute
                if ':' in s:
                    hour_str, minute_str = s.split(':', 1)
                else:
                    hour_str, minute_str = s, '0'
                hour = int(hour_str)
                minute = int(minute_str)
                if am_pm == 'PM' and hour != 12:
                    hour += 12
                if am_pm == 'AM' and hour == 12:
                    hour = 0
                return f"{hour:02d}", f"{minute:02d}"
            else:
                # 24‑hour format (with or without colon)
                if ':' in s:
                    hour_str, minute_str = s.split(':', 1)
                else:
                    hour_str, minute_str = s, '0'
                hour = int(hour_str)
                minute = int(minute_str)
                return f"{hour:02d}", f"{minute:02d}"
        except Exception:
            logger.error(f"⚠️ Could not parse time string '{time_str}'. Leaving unchanged.")
            return None, None

    # ------------------------------------------------------------------
    # 🔧 Helper methods for CSV-based date updates
    #
    # The following methods provide a basic implementation for automating
    # date updates in the D2L Manage Dates interface using Playwright.
    # They are intentionally conservative: they attempt straightforward
    # selectors and log their progress.  If a selector fails, the error
    # is logged and the script continues to the next assignment.  These
    # methods can be extended with more robust fuzzy matching and
    # additional fallback strategies as needed.

    async def perform_date_updates(self, page, assignments: list[dict]):
        """
        Iterate over each assignment dictionary and attempt to update the
        corresponding start and due dates on the Manage Dates page.  Each
        dictionary should include ``assignment`` (name), ``start_date``,
        ``due_date`` and optionally ``end_date`` fields.  If a given
        date field is empty, it is skipped.  Successful updates and
        failures are logged; the function does not throw unless an
        unexpected Playwright error occurs.

        Parameters
        ----------
        page : playwright.async_api.Page
            The already loaded Manage Dates page.
        assignments : list of dict
            A list of assignments as parsed from the CSV file.
        """
        for idx, assignment_info in enumerate(assignments, start=1):
            name = assignment_info.get('assignment', '').strip()
            start_date_str = assignment_info.get('start_date', '').strip()
            due_date_str = assignment_info.get('due_date', '').strip()
            end_date_str = assignment_info.get('end_date', '').strip()
            if not name:
                logger.warning(f"Row {idx}: Empty assignment name – skipping.")
                continue
            logger.info(f"➡️ Updating assignment '{name}' (Row {idx})")
            logger.debug(f"📂 Raw row data: {assignment_info}")
            logger.info(f"🔍 Locating assignment row for '{name}'...")
            # Locate the table row for this assignment
            row = await self.find_assignment_row(page, name)
            if not row:
                logger.warning(f"Row {idx}: Assignment '{name}' not found on page – skipping.")
                continue
            # Due date update
            due_time_str = assignment_info.get('due_time', '').strip() if assignment_info.get('due_time') else ''
            # Treat 'nan' as empty (common in CSV exports)
            if due_date_str and due_date_str.lower() == 'nan':
                due_date_str = ''
            if due_time_str and due_time_str.lower() == 'nan':
                due_time_str = ''
            logger.debug(f"🔍 Due date check: due_date_str='{due_date_str}' (len={len(due_date_str) if due_date_str else 0})")
            if due_date_str:
                try:
                    await self.update_due_date(page, row, due_date_str, due_time_str)
                    logger.info(f"✅ Due date updated for '{name}' → {due_date_str}{(' ' + due_time_str) if due_time_str else ''}")
                except Exception as err:
                    logger.error(f"❌ Failed to update due date for '{name}': {err}")
            else:
                logger.debug(f"🔍 Skipping due date for '{name}' - no due date provided")
            # Start date update
            start_time_str = assignment_info.get('start_time', '').strip() if assignment_info.get('start_time') else ''
            # Treat 'nan' as empty (common in CSV exports)
            if start_date_str and start_date_str.lower() == 'nan':
                start_date_str = ''
            if start_time_str and start_time_str.lower() == 'nan':
                start_time_str = ''
            logger.debug(f"🔍 Start date check: start_date_str='{start_date_str}' (len={len(start_date_str) if start_date_str else 0})")
            if start_date_str:
                try:
                    await self.update_start_date(page, row, start_date_str, start_time_str)
                    logger.info(f"✅ Start date updated for '{name}' → {start_date_str}{(' ' + start_time_str) if start_time_str else ''}")
                except Exception as err:
                    logger.error(f"❌ Failed to update start date for '{name}': {err}")
            else:
                logger.debug(f"🔍 Skipping start date for '{name}' - no start date provided")

    async def find_assignment_row(self, page, assignment_name: str):
        """
        Attempt to locate the table row containing the assignment name.  This
        method uses a simple text match and then returns the ``<tr>``
        element.  It first tries an exact substring match; if that fails,
        it removes dashes (–—−) and quotes from the search term and tries
        again.  If still not found, None is returned.

        Parameters
        ----------
        page : playwright.async_api.Page
            The Manage Dates page.
        assignment_name : str
            The exact (or near‑exact) name of the assignment.

        Returns
        -------
        playwright.async_api.ElementHandle | None
            The row element if found; otherwise None.
        """
        # Attempt exact match
        selectors = [assignment_name]
        import re
        # Also search for versions without dashes and quotes
        name_no_dash = re.sub(r'[-–—−]', ' ', assignment_name).strip()
        if name_no_dash.lower() != assignment_name.lower():
            selectors.append(name_no_dash)
        clean_name = assignment_name.replace("'", '').replace('"', '')
        if clean_name.lower() not in (assignment_name.lower(), name_no_dash.lower()):
            selectors.append(clean_name)
        for search_term in selectors:
            try:
                # Lower-case the search term for case-insensitive matching.
                lower_term = search_term.lower()
                # Debug: Check if any elements match the base selector first
                base_elements = await page.query_selector_all("//td[contains(@class, 'd_dg_col_Name')]//a")
                logger.debug(f"🔍 Found {len(base_elements)} base assignment links for search term '{search_term}'")
                
                # Debug: Log the text content of the first few base elements
                for i, elem in enumerate(base_elements[:3]):
                    try:
                        text = await elem.text_content()
                        logger.debug(f"🔍 Base element {i+1}: '{text.strip()}'")
                    except:
                        logger.debug(f"🔍 Base element {i+1}: Could not get text")
                
                # Try a simpler approach: search through all elements manually
                for elem in base_elements:
                    try:
                        text = await elem.text_content()
                        if text and lower_term in text.lower():
                            logger.debug(f"✅ Found matching element: '{text.strip()}'")
                            # Get the parent row using XPath
                            try:
                                row = await elem.evaluate_handle("element => element.closest('tr')")
                                if row:
                                    logger.info(f"✅ Assignment row found using search term '{search_term}'.")
                                    return row
                            except Exception as ex:
                                logger.debug(f"⚠️ Exception getting parent row: {ex}")
                                # Try alternative approach
                                try:
                                    row = await elem.evaluate_handle("element => element.parentElement.closest('tr')")
                                    if row:
                                        logger.info(f"✅ Assignment row found using search term '{search_term}'.")
                                        return row
                                except Exception as ex2:
                                    logger.debug(f"⚠️ Alternative approach also failed: {ex2}")
                                    continue
                    except Exception as ex:
                        logger.debug(f"⚠️ Exception checking element: {ex}")
                        continue
                
                # Fallback to original XPath if manual search fails
                xpath = (
                    "//td[contains(@class, 'd_dg_col_Name')]//a["
                    "contains(translate(normalize-space(text()), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '"
                    + lower_term + "')]/ancestor::tr"
                )
                logger.debug(f"🔎 Trying XPath fallback: {xpath}")
                row = await page.query_selector(xpath)
                if row:
                    logger.info(f"✅ Assignment row found using search term '{search_term}'.")
                    return row
            except Exception as ex:
                logger.debug(f"⚠️ Exception during row search with term '{search_term}': {ex}")
                continue
        return None

    async def update_due_date(self, page, row, date_str: str, time_str: str = ''):
        """
        Click the due date link in the provided row, then set the new date (and
        optionally the time) in the ensuing dialog and save.  If
        ``time_str`` is blank or missing, the time fields are left
        unchanged.

        Parameters
        ----------
        page : playwright.async_api.Page
            The Manage Dates page.
        row : playwright.async_api.ElementHandle
            The table row containing the assignment.
        date_str : str
            The date string in a format accepted by the D2L date picker.
        time_str : str, optional
            A time string (e.g. '2:30 PM', '14:30') to set.  If omitted or
            empty, no changes will be made to the time fields.
        """
        # Find the due date cell/link; it may be a dash or a date
        due_link = await row.query_selector("xpath=.//td[contains(@class, 'd_dg_col_DueDate')]//a")
        if not due_link:
            # Fallback: any anchor in the row with title 'Edit the due date'
            due_link = await row.query_selector("xpath=.//a[@title='Edit the due date']")
        if not due_link:
            raise RuntimeError("Due date link not found")
        logger.info("🖱️ Clicking due date link...")
        await due_link.click()
        # Wait for the dialog
        dialog = await page.wait_for_selector("[role='dialog']", timeout=8000)
        logger.info("📋 Due date dialog opened. Setting date/time...")
        # Determine hour/minute from time_str
        hour, minute = self._parse_time_str(time_str) if time_str else (None, None)
        # Fill the date/time fields inside the iframe.  If no time provided, None values
        # will prevent the time fields from being modified.
        await self.set_date_in_dialog(page, dialog, date_str, hour=hour, minute=minute, check_selector="#z_k")
        logger.info("💾 Due date dialog processed (save attempted).")

    async def update_start_date(self, page, row, date_str: str, time_str: str = ''):
        """
        Click the start date link in the provided row, then set the new date
        (and optionally the time) in the ensuing dialog and save.  If
        ``time_str`` is blank or missing, the time fields are left
        unchanged.  The start date checkbox is automatically checked if
        present.
        """
        start_link = await row.query_selector("xpath=.//td[contains(@class, 'd_dg_col_StartDate')]//a")
        if not start_link:
            # Fallback: anchor with title 'Edit the start date'
            start_link = await row.query_selector("xpath=.//a[@title='Edit the start date']")
        if not start_link:
            raise RuntimeError("Start date link not found")
        logger.info("🖱️ Clicking start date link...")
        await start_link.click()
        dialog = await page.wait_for_selector("[role='dialog']", timeout=8000)
        logger.info("📋 Start date dialog opened. Setting date/time...")
        # Determine hour/minute from time_str
        hour, minute = self._parse_time_str(time_str) if time_str else (None, None)
        # Use checkbox id 'z_o' for start date; D2L uses this id for the "Has Start Date" checkbox
        await self.set_date_in_dialog(page, dialog, date_str, hour=hour, minute=minute, check_selector="#z_o")
        logger.info("💾 Start date dialog processed (save attempted).")

    async def set_date_in_dialog(self, page, dialog, date_str: str, hour, minute, check_selector: str):
        """
        Helper to set date and time inside the date picker dialog.  It
        switches into the first iframe containing date fields, checks the
        appropriate checkbox (if not already checked) and fills year,
        month, day, hour, minute.  After setting values it clicks the Save
        button outside the iframe.  The checkbox selector should be '#z_k'
        for due date and '#z_o' for start date.

        Parameters
        ----------
        page : playwright.async_api.Page
            The current page.
        dialog : playwright.async_api.ElementHandle
            The dialog element with role='dialog'.
        date_str : str
            The date string to set (e.g., '2025-10-19' or '10/19/2025').
        hour : str or None
            Hour in 24‑hour format to set (e.g., '23' for 11 PM).  If None,
            the hour field is not modified.
        minute : str or None
            Minute to set (e.g., '59').  If None, the minute field is not
            modified.
        check_selector : str
            CSS selector for the date checkbox inside the iframe ('#z_k' for due, '#z_o' for start).
        """
        # Determine month/day/year
        try:
            import datetime
            if '/' in date_str:
                parts = [p.strip() for p in date_str.split('/')]
                if len(parts) == 3:
                    month, day, year = parts
                else:
                    # Unknown format; fallback to parsing as ISO
                    dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                    month, day, year = str(dt.month), str(dt.day), str(dt.year)
            elif '-' in date_str:
                dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                month, day, year = str(dt.month), str(dt.day), str(dt.year)
            else:
                # Try parsing as 'Month dd, yyyy'
                dt = datetime.datetime.strptime(date_str, '%B %d, %Y')
                month, day, year = str(dt.month), str(dt.day), str(dt.year)
        except Exception:
            logger.error(f"⚠️ Could not parse date '{date_str}'. Using as-is.")
            month = day = year = ''
        # Log the parsed date/time values for debugging
        try:
            logger.debug(f"🗓️ Parsed date: {month}/{day}/{year}, time: {hour}:{minute}")
        except Exception:
            pass
        logger.debug(f"🗓️ Parsing date string '{date_str}' → {month}/{day}/{year} (if available)")
        # Find the iframe containing the date fields
        iframes = await dialog.query_selector_all("iframe")
        logger.debug(f"🔍 Found {len(iframes)} iframes in dialog")
        
        # Debug: Check what's actually in the dialog (not just iframe)
        all_dialog_inputs = await dialog.query_selector_all("input")
        logger.debug(f"🔍 Dialog has {len(all_dialog_inputs)} input fields directly")
        for j, inp in enumerate(all_dialog_inputs[:3]):
            try:
                name = await inp.get_attribute("name")
                input_type = await inp.get_attribute("type")
                logger.debug(f"🔍 Dialog Input {j+1}: name='{name}', type='{input_type}'")
            except:
                logger.debug(f"🔍 Dialog Input {j+1}: Could not get attributes")
        
        target_frame = None
        for i, frame_element in enumerate(iframes):
            try:
                # Debug: Check iframe attributes
                iframe_src = await frame_element.get_attribute("src")
                iframe_title = await frame_element.get_attribute("title")
                logger.debug(f"🔍 Iframe {i+1}: src='{iframe_src}', title='{iframe_title}'")
                
                # Wait for iframe to load content properly
                logger.debug(f"⏳ Waiting for iframe {i+1} content to load...")
                await frame_element.wait_for_element_state("visible", timeout=10000)
                
                # Wait for iframe to have actual content (not just blank)
                for attempt in range(10):  # Try up to 10 times (10 seconds total)
                    frame = await frame_element.content_frame()
                    if frame:
                        # Check if iframe has meaningful content
                        all_elements = await frame.query_selector_all("*")
                        all_inputs = await frame.query_selector_all("input")
                        logger.debug(f"🔍 Iframe {i+1} attempt {attempt+1}: {len(all_elements)} elements, {len(all_inputs)} inputs")
                        
                        # If we have inputs, the iframe is loaded
                        if len(all_inputs) > 0:
                            logger.debug(f"✅ Iframe {i+1} loaded with {len(all_inputs)} input fields")
                            break
                        elif len(all_elements) > 5:  # More than just basic HTML structure
                            logger.debug(f"✅ Iframe {i+1} loaded with {len(all_elements)} elements")
                            break
                        else:
                            logger.debug(f"⏳ Iframe {i+1} still loading... waiting 1 second")
                            await asyncio.sleep(1)
                    else:
                        logger.debug(f"⏳ Iframe {i+1} frame not ready... waiting 1 second")
                        await asyncio.sleep(1)
                
                frame = await frame_element.content_frame()
                logger.debug(f"🔍 Checking iframe {i+1}...")
                
                # Debug: Log ALL elements in iframe, not just inputs
                all_elements = await frame.query_selector_all("*")
                logger.debug(f"🔍 Iframe {i+1} has {len(all_elements)} total elements")
                
                # Debug: Log all input fields in this iframe
                all_inputs = await frame.query_selector_all("input")
                logger.debug(f"🔍 Iframe {i+1} has {len(all_inputs)} input fields")
                for j, inp in enumerate(all_inputs[:5]):  # Show first 5 inputs
                    try:
                        name = await inp.get_attribute("name")
                        input_type = await inp.get_attribute("type")
                        logger.debug(f"🔍 Input {j+1}: name='{name}', type='{input_type}'")
                    except:
                        logger.debug(f"🔍 Input {j+1}: Could not get attributes")
                
                # Debug: Check for ANY form elements
                forms = await frame.query_selector_all("form")
                selects = await frame.query_selector_all("select")
                buttons = await frame.query_selector_all("button")
                logger.debug(f"🔍 Iframe {i+1} has {len(forms)} forms, {len(selects)} selects, {len(buttons)} buttons")
                
                # Check for the actual D2L date field - single text input with M/D/YYYY placeholder
                date_field = await frame.query_selector("input[placeholder='M/D/YYYY']:not([type='hidden'])")
                time_field = await frame.query_selector("input[aria-label*='Time']:not([type='hidden'])") or await frame.query_selector("input[placeholder*='time']:not([type='hidden'])")
                
                if date_field:
                    logger.debug("✅ Found iframe with date field.")
                    target_frame = frame
                    break
                else:
                    logger.debug(f"⚠️ Iframe {i+1} missing date field: date={date_field is not None}")
            except Exception as ex:
                logger.debug(f"⚠️ Exception checking iframe {i+1}: {ex}")
                continue
        if not target_frame:
            logger.error("❌ No iframe with date fields found in dialog.")
            raise RuntimeError("No iframe with date fields found")
        # Check the date checkbox if necessary
        try:
            checkbox = await target_frame.query_selector(check_selector)
            if checkbox:
                checked = await checkbox.is_checked()
                if not checked:
                    await checkbox.check()
                    logger.debug(f"☑️ Checked checkbox {check_selector} in date dialog.")
        except Exception:
            pass
        # Fill the actual D2L date field - single text input
        try:
            # Check if frame is still attached before filling
            logger.debug(f"🔍 Checking frame detachment status...")
            try:
                frame_detached = target_frame.is_detached()
                logger.debug(f"🔍 Frame detachment check result: {frame_detached}")
            except Exception as frame_check_err:
                logger.debug(f"⚠️ Exception checking frame detachment: {frame_check_err}")
                frame_detached = True  # Assume detached if we can't check
                logger.debug(f"🔍 Assuming frame is detached due to error")
            
            if not frame_detached:
                logger.debug(f"🔍 Frame is still attached, proceeding with field filling...")
                # Fill the date field with M/D/YYYY format
                if month and day and year:
                    date_value = f"{month}/{day}/{year}"
                    await target_frame.fill("input[placeholder='M/D/YYYY']:not([type='hidden'])", date_value)
                    logger.debug(f"🖊️ Filled date field: {date_value}")
                
                # Fill time field if available - D2L time dropdown
                if hour is not None and minute is not None:
                    # Convert to 12-hour format (AM/PM)
                    try:
                        hour_int = int(hour)
                        minute_int = int(minute)
                        
                        # Convert 24-hour to 12-hour format
                        if hour_int == 0:
                            display_hour = 12
                            period = "AM"
                        elif hour_int < 12:
                            display_hour = hour_int
                            period = "AM"
                        elif hour_int == 12:
                            display_hour = 12
                            period = "PM"
                        else:
                            display_hour = hour_int - 12
                            period = "PM"
                        
                        time_value = f"{display_hour}:{minute_int:02d} {period}"
                    except (ValueError, TypeError):
                        # If conversion fails, use the original values
                        time_value = f"{hour}:{minute}"
                    
                    # Try multiple selectors for the time dropdown
                    time_selectors = [
                        "input[role='combobox'][class*='d2l-dropdown-opener']",  # D2L time dropdown
                        "input[aria-controls*='timezone']",  # Time field with timezone control
                        "input[class*='d2l-dropdown-opener']",  # Any D2L dropdown opener
                        "input[aria-label*='Time']"  # Fallback
                    ]
                    
                    time_filled = False
                    for selector in time_selectors:
                        try:
                            await target_frame.fill(selector, time_value)
                            logger.debug(f"🖊️ Filled time field using '{selector}': {time_value}")
                            time_filled = True
                            break
                        except Exception:
                            continue
                    
                    if not time_filled:
                        logger.debug(f"⚠️ Could not find time field to fill with: {time_value}")
                logger.debug(f"🔍 Completed field filling, about to exit try block...")
            else:
                logger.error("❌ Frame was detached before filling fields")
        except Exception as fill_err:
            logger.error(f"⚠️ Error filling date/time fields: {fill_err}")
            logger.debug(f"🔍 Exception details: {type(fill_err).__name__}: {fill_err}")
        
        # Debug: Check if we're reaching the save button section
        logger.debug(f"🔍 Reached save button section - about to look for save button...")
        
        # Save the date: click save button in the main dialog (NOT in iframe)
        await page.wait_for_timeout(200)  # small delay
        
        # Debug: Check iframe context and find save button
        logger.debug(f"🔍 Looking for save button in main dialog...")
        # Note: We're now in main dialog context, not iframe context
        logger.debug(f"🔍 Searching for save button in main page context...")
        
        # Save button is in the main dialog, not in the iframe
        save_selectors = [
            "button.d2l-button[primary='']",  # Exact match for D2L save button
            "button[class='d2l-button'][primary='']",  # More specific
            "button.d2l-button",  # Any D2L button
            "//button[text()='Save']",  # Fallback to text
            "//button[contains(text(), 'Save')]"  # Fallback to partial text
        ]
        
        save_clicked = False
        for selector in save_selectors:
            try:
                logger.debug(f"🔍 Trying save selector: '{selector}'")
                btn = await page.query_selector(selector)  # Look in main page, not iframe
                if btn:
                    logger.debug(f"✅ Found save button with selector: '{selector}'")
                    await btn.click()
                    logger.debug(f"💾 Clicked save button using selector '{selector}'.")
                    save_clicked = True
                    break
                else:
                    logger.debug(f"❌ No save button found with selector: '{selector}'")
            except Exception as e:
                logger.debug(f"⚠️ Exception with save selector '{selector}': {e}")
                continue
        
        if not save_clicked:
            logger.error("❌ Could not find save button in main dialog")
        await page.wait_for_timeout(500)


# ========================================
# 🚀 CLI ENTRY POINT
# ========================================
if __name__ == "__main__":
    try:
        logger.info("🐍 D2L Processor started via CLI.")
        action = sys.argv[1] if len(sys.argv) > 1 else "login"
        course_code = sys.argv[2] if len(sys.argv) > 2 else None
        # Support optional CSV path for the process action
        csv_path = sys.argv[3] if len(sys.argv) > 3 else None
        processor = D2LProcessor()
        success = processor.run_automation(action, course_code, csv_path)
        # Emit a trailing JSON line to allow callers (Node) to parse results
        result = {
            "success": success,
            "message": "D2L automation completed" if success else "D2L automation failed",
            "action": action,
            "course": course_code,
            "csv": csv_path,
            # include how many assignments were processed (logged) if available
            "processed": getattr(processor, "assignments_processed", None)
        }
        print(json.dumps(result))
    except Exception as e:
        logger.error(f"❌ Fatal D2L Processor Error: {e}")
        traceback.print_exc()