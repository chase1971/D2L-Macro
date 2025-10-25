# 🧩 PROJECT STRUCTURE SUMMARY
**Generated:** 2025-10-25 15:25:52

## 🚀 APPLICATION OVERVIEW

### Purpose
This application is a **D2L Course Management Automation Tool** that automates assignment date updates in the Desire2Learn (D2L) learning management system using browser automation.

**Key Capabilities:**
- Browser automation for D2L course management
- Persistent login session management
- Automated assignment date modification

### Key Components

### Architecture Summary
- **Total Modules**: 2
- **Total Functions**: 33
- **Total Classes**: 3

### Key Features
- Assignment Date Automation
- Browser Automation
- D2L Course Management
- Documentation Generation

### 📄 Project Structure & Examples
**Example Module: `example.py`**
*Purpose: D2L assignment date automation and management.*

**Key Functions:**
- `__init__`
- `browse_csv_file`
- `cleanup_existing_processes`

**Function Signatures:**
```python
D2LDateProcessor.__init__(self) -> None
D2LDateProcessor.find_assignment_due_date_link(self, assignment_name) -> None
D2LDateProcessor.find_assignment_start_date_link(self, assignment_name) -> None
D2LDateProcessor.process_csv_file(self, csv_file_path) -> None
D2LDateProcessor.set_assignment_due_date(self, assignment_name, due_date, due_time) -> None
```

**Project Statistics:**
- **Total Modules**: 2
- **Total Functions**: 33
- **Total Classes**: 3

---

## 🚪 ENTRY POINTS

### Utility Scripts
- **`d2l_date_processing.py`**: D2L assignment date automation and management.
- **`d2l_playwright_processor.py`**: D2L browser automation using Playwright. Provides asynchronous operations.

### Execution Flow
1. **Start**: Launch the D2L automation tool
3. **Login**: Authenticate with D2L learning management system
4. **Course Selection**: Navigate to the target course
7. **Completion**: Verify updates and close browser session

### Command Line Usage
```bash
# Run D2L date processing
python d2l_date_processing_new.py

# Run Playwright automation
python d2l_playwright_processor.py
```

---

## 🔄 SHARED STATE TABLE

| File | Variable | Modified By | Read By |
|------|----------|-------------|---------|
| d2l_playwright_processor.py | `logger` | - | _parse_time_str +5 more, _write_debug_report, automate_d2l, open_course, process_course, run_automation |

---

This document provides a full architectural map of the project.

## 🧱 Module Dependency Graph

```mermaid
graph TD
```

## 🔄 Cross-Module Data Flow Map

| Source Module | Target or Description |
|----------------|----------------------|
| d2l_date_processing.py | Functions: __init__, browse_csv_file, cleanup_existing_processes, clear_login, create_widgets, exit_app, find_assignment_due_date_link, find_assignment_start_date_link, login_to_d2l, main, process_csv, process_c... |
| d2l_playwright_processor.py | Functions: __init__, _parse_time_str, _write_debug_report, automate_d2l, find_assignment_row, open_course, perform_date_updates, process_course, run_automation, set_date_in_dialog, update_due_date, update_start_... |

## 📦 Module Summaries

### `d2l_date_processing.py`

**Intent:** D2L assignment date automation and management.

**Classes:** D2LDateProcessor, D2LDateProcessorGUI

**Functions:** __init__, browse_csv_file, cleanup_existing_processes, clear_login, create_widgets, exit_app, find_assignment_due_date_link, find_assignment_start_date_link, login_to_d2l, main, process_csv, process_csv_file, run, set_assignment_due_date, set_assignment_start_date, set_date_in_iframe, set_date_in_mini_editor, set_start_date_in_mini_editor, setup_driver, setup_logging, update_status

**Globals:** _None_


**Local Imports:** _None_

**External Imports:** csv, datetime, logging, os, psutil, re, selenium, selenium.common.exceptions, selenium.webdriver.chrome.options, selenium.webdriver.chrome.service, selenium.webdriver.common.by, selenium.webdriver.support, selenium.webdriver.support.ui, shutil, subprocess, tempfile, threading, time, tkinter, webdriver_manager.chrome


#### 📝 Function Signatures

- `D2LDateProcessor.__init__(self) -> None`

- `D2LDateProcessor.find_assignment_due_date_link(self, assignment_name) -> None`

- `D2LDateProcessor.find_assignment_start_date_link(self, assignment_name) -> None`

- `D2LDateProcessor.process_csv_file(self, csv_file_path) -> None`

- `D2LDateProcessor.set_assignment_due_date(self, assignment_name, due_date, due_time) -> None`

- `D2LDateProcessor.set_assignment_start_date(self, assignment_name, start_date, start_time) -> None`

- `D2LDateProcessor.set_date_in_iframe(self, new_date, new_time, checkbox_id = None) -> None`

- `D2LDateProcessor.set_date_in_mini_editor(self, new_date, new_time) -> None`

- `D2LDateProcessor.set_start_date_in_mini_editor(self, new_date, new_time) -> None`

- `D2LDateProcessor.setup_driver(self, use_profile = True) -> None`

- `D2LDateProcessor.setup_logging(self) -> None`

- `D2LDateProcessorGUI.__init__(self) -> None`

- `D2LDateProcessorGUI.browse_csv_file(self) -> None`

- `D2LDateProcessorGUI.clear_login(self) -> None`

- `D2LDateProcessorGUI.create_widgets(self) -> None`

- `D2LDateProcessorGUI.exit_app(self) -> None`

- `D2LDateProcessorGUI.login_to_d2l(self) -> None`

- `D2LDateProcessorGUI.process_csv(self) -> None`

- `D2LDateProcessorGUI.run(self) -> None`

- `D2LDateProcessorGUI.update_status(self, message) -> None`

- `cleanup_existing_processes() -> None`

- `main() -> None`


#### 🎯 Function Intents

- **__init__()**: Handles the target entities.

- **browse_csv_file()**: Browse for CSV file.

- **cleanup_existing_processes()**: Clean up any existing Chrome/ChromeDriver processes.

- **clear_login()**: Clear saved login session.

- **create_widgets()**: Create the GUI widgets.

- **exit_app()**: Exit the application.

- **find_assignment_due_date_link()**: Find the due date link for a specific assignment by name with fuzzy matching.

- **find_assignment_start_date_link()**: Find the start date link for a specific assignment by name with fuzzy matching.

- **login_to_d2l()**: Handle login process.

- **main()**: Main function.

- **process_csv()**: Process the CSV file.

- **process_csv_file()**: Process CSV file and update assignments.

- **run()**: Start the GUI.

- **set_assignment_due_date()**: Set due date for a specific assignment.

- **set_assignment_start_date()**: Set start date for a specific assignment.

- **set_date_in_iframe()**: Set date and time in the iframe.

- **set_date_in_mini_editor()**: Set date and time in the mini editor popup.

- **set_start_date_in_mini_editor()**: Set start date in mini editor - handles start date checkbox.

- **setup_driver()**: Setup Chrome driver with persistent login session.

- **setup_logging()**: Setup logging configuration.

- **update_status()**: Update the status label and log.


#### File I/O Summary

- Reads: unknown

- Writes: _None_


#### Threading & UI Bindings

- Threads: _None_

- UI Binds: _None_


#### Exception Paths

line 1088: ['all exceptions'], line 51: ['Exception'], line 96: ['Exception'], line 199: ['Exception'], line 222: ['Exception'], line 261: ['Exception'], line 406: ['Exception'], line 557: ['Exception'], line 608: ['Exception'], line 681: ['Exception'], line 1001: ['Exception'], line 1025: ['Exception'], line 1051: ['Exception'], line 1073: ['all exceptions'], line 1089: ['ImportError'], line 74: ['Exception'], line 233: ['Exception'], line 685: ['Exception'], line 730: ['Exception'], line 860: ['Exception'], line 600: ['all exceptions'], line 624: ['all exceptions'], line 673: ['all exceptions'], line 892: ['all exceptions'], line 1095: ['all exceptions'], line 113: ['Exception'], line 239: ['Exception'], line 281: ['all exceptions'], line 317: ['all exceptions'], line 373: ['Exception'], line 428: ['all exceptions'], line 466: ['all exceptions'], line 489: ['Exception'], line 528: ['Exception'], line 871: ['all exceptions'], line 745: ['Exception'], line 765: ['Exception'], line 146: ['Exception']


---

### `d2l_playwright_processor.py`

**Intent:** D2L browser automation using Playwright. Provides asynchronous operations.

**Classes:** D2LProcessor

**Functions:** __init__, _parse_time_str, _write_debug_report, automate_d2l, find_assignment_row, open_course, perform_date_updates, process_course, run_automation, set_date_in_dialog, update_due_date, update_start_date

**Globals:** COURSE_URLS, D2L_BASE_URL, LOGS_DIR, LOG_PATH, SHARED_BROWSER_DIR, action, course_code, csv_path, logger, processor, result, success


**Local Imports:** _None_

**External Imports:** asyncio, csv, datetime, json, logging, os, pandas, playwright.async_api, re, subprocess, sys, traceback


#### 📝 Function Signatures

- `D2LProcessor.__init__(self) -> None`

- `D2LProcessor._parse_time_str(self, time_str: str) -> None`

- `D2LProcessor._write_debug_report(self, stage, exception) -> None`

- `D2LProcessor.run_automation(self, action = None, course_code = None, csv_path = None) -> None`


#### 🎯 Function Intents

- **__init__()**: Handles the target entities.

- **_parse_time_str()**: Parse a time string from the CSV into a 24‑hour hour and minute pair.

- **_write_debug_report()**: Write detailed debug info to a file and launch Notepad to display it.

- **automate_d2l()**: Main coroutine that attaches to an existing Chrome instance and performs.

- **find_assignment_row()**: Attempt to locate the table row containing the assignment name.

- **open_course()**: Navigate to a specific course page.

- **perform_date_updates()**: Iterate over each assignment dictionary and attempt to update the.

- **process_course()**: Open the course manage-dates page and prepare to process a CSV.

- **run_automation()**: Launch the automation coroutine and handle cleanup.

- **set_date_in_dialog()**: Helper to set date and time inside the date picker dialog.

- **update_due_date()**: Click the due date link in the provided row; then set the new date (and.

- **update_start_date()**: Click the start date link in the provided row; then set the new date.


#### File I/O Summary

- Reads: _None_

- Writes: _None_


#### Threading & UI Bindings

- Threads: _None_

- UI Binds: _None_


#### Exception Paths

line 944: ['Exception'], line 114: ['Exception'], line 166: ['Exception'], line 202: ['Exception'], line 347: ['SystemExit', 'Exception'], line 375: ['Exception'], line 410: ['Exception'], line 699: ['Exception'], line 720: ['Exception'], line 816: ['Exception'], line 826: ['Exception'], line 122: ['Exception'], line 360: ['Exception'], line 552: ['Exception'], line 733: ['all exceptions'], line 742: ['Exception'], line 829: ['Exception'], line 920: ['Exception'], line 247: ['all exceptions'], line 259: ['Exception'], line 327: ['Exception'], line 497: ['Exception'], line 513: ['Exception'], line 261: ['ImportError'], line 561: ['all exceptions'], line 569: ['Exception'], line 786: ['all exceptions'], line 848: ['ValueError', 'TypeError'], line 881: ['Exception'], line 574: ['Exception'], line 582: ['Exception']


---

## 🧠 DATA SCHEMA SUMMARY

```json
{
  "ModuleSummary": {
    "file": "str",
    "classes": ["list[str]"],
    "functions": ["list[str]"],
    "globals": ["list[str]"],
    "imports_local": ["list[str]"],
    "imports_external": ["list[str]"],
    "io_reads": ["list[str]"],
    "io_writes": ["list[str]"],
    "threads": ["list[str]"],
    "ui_binds": ["list[str]"],
    "exceptions": ["list[str]"],
    "intent": "str",
    "function_signatures": ["list[str]"],
    "function_intents": "str"
  }
}
```
