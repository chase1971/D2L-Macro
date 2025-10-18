#!/usr/bin/env python3
"""
D2L Playwright Processor (Fixed to match Automation Agent behavior)
------------------------------------------------------------------
- Connects ONLY to the Chrome instance launched by Node.
- Does NOT start its own Chromium (avoids blue icon & file locks).
- Keeps session persistent using Shared-Browser-Data.
- Provides clear logging if Chrome is not running.
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

LOG_PATH = os.path.join(os.path.dirname(__file__), "d2l_processor.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ========================================
# 🧠 MAIN CLASS
# ========================================

class D2LProcessor:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def automate_d2l(self, action=None, course_code=None):
        """Main coroutine that connects to Chrome and performs automation."""
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
            else:
                # Normal login flow — go to D2L home page
                logger.info(f"🌍 Navigating to D2L base URL: {D2L_BASE_URL}")
                await self.page.goto(D2L_BASE_URL, wait_until="networkidle")
                await asyncio.sleep(3)
                logger.info("✅ Browser ready for manual login.")
                logger.info("🕓 Holding browser open indefinitely (D2L session active).")
                await asyncio.Event().wait()

        except Exception as e:
            self._write_debug_report("automate_d2l", e)
            raise

    async def open_course(self, course_code: str):
        """Navigate to specific course page."""
        try:
            if not self.context:
                raise RuntimeError("Browser not initialized.")
            url = COURSE_URLS.get(course_code)
            if not url:
                raise KeyError(f"Course {course_code} not found.")
            page = self.context.pages[0] if self.context.pages else await self.context.new_page()
            logger.info(f"📘 Opening course page: {url}")
            await page.goto(url, wait_until='networkidle')
            await asyncio.sleep(3)
            logger.info(f"✅ Course {course_code} loaded successfully.")
        except Exception as e:
            self._write_debug_report("open_course", e)
            raise

    def run_automation(self, action=None, course_code=None):
        """Launch coroutine safely."""
        try:
            logger.info("🧠 Starting D2L automation process...")
            asyncio.run(self.automate_d2l(action, course_code))
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
        """Write detailed debug info to file."""
        try:
            debug_dir = os.path.join(os.path.dirname(__file__), "debug_logs")
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

# ========================================
# 🚀 CLI ENTRY POINT
# ========================================

if __name__ == "__main__":
    try:
        logger.info("🐍 D2L Processor started via CLI.")
        action = sys.argv[1] if len(sys.argv) > 1 else "login"
        course_code = sys.argv[2] if len(sys.argv) > 2 else None

        processor = D2LProcessor()
        success = processor.run_automation(action, course_code)

        result = {"success": success, "message": "D2L Automation completed" if success else "D2L Automation failed"}
        print(json.dumps(result))
    except Exception as e:
        logger.error(f"❌ Fatal D2L Processor Error: {e}")
        traceback.print_exc()
