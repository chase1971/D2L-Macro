# 🧩 PROJECT STRUCTURE SUMMARY
**Generated:** 2025-10-24 23:36:24

This document provides a full architectural map of the project.

## 🧱 Module Dependency Graph

```mermaid
graph TD
```

## 🔄 Cross-Module Data Flow Map

| Source Module | Target or Description |
|----------------|----------------------|
| D2L_Gui.py | Functions: __init__, async_navigation, browse_csv_file, cleanup_existing_processes, clear_login, exit_app, go_to_class, login_to_d2l, main, run, run_async_navigation, setup_browser, setup_gui, setup_logging, upd... |
| d2l_date_processing.py | Functions: __init__, browse_csv_file, cleanup_existing_processes, clear_login, create_widgets, exit_app, find_assignment_due_date_link, find_assignment_start_date_link, login_to_d2l, main, process_csv, process_c... |
| d2l_date_processing_new.py | Functions: __init__, close, process_csv_file, set_assignment_due_date, set_assignment_start_date, setup_driver |
| d2l_playwright_processor.py | Functions: __init__, _parse_time_str, _write_debug_report, automate_d2l, find_assignment_row, open_course, perform_date_updates, process_course, run_automation, set_date_in_dialog, update_due_date, update_start_... |

## 📦 Module Summaries

### `d2l_date_processing.py`

**Intent:** Creates and manages user interface components for date and assignment operations.

**Classes:** D2LDateProcessor, D2LDateProcessorGUI

**Functions:** __init__, browse_csv_file, cleanup_existing_processes, clear_login, create_widgets, exit_app, find_assignment_due_date_link, find_assignment_start_date_link, login_to_d2l, main, process_csv, process_csv_file, run, set_assignment_due_date, set_assignment_start_date, set_date_in_iframe, set_date_in_mini_editor, set_start_date_in_mini_editor, setup_driver, setup_logging, update_status

**Globals:** _None_


**Local Imports:** _None_

**External Imports:** csv, datetime, logging, os, psutil, re, selenium, selenium.common.exceptions, selenium.webdriver.chrome.options, selenium.webdriver.chrome.service, selenium.webdriver.common.by, selenium.webdriver.support, selenium.webdriver.support.ui, shutil, subprocess, tempfile, threading, time, tkinter, webdriver_manager.chrome


#### File I/O Summary

- Reads: _None_

- Writes: _None_


#### Threading & UI Bindings

- Threads: _None_

- UI Binds: _None_


#### Exception Paths

_No exception handlers detected._


---

### `d2l_date_processing_new.py`

**Intent:** Sets, Sets up assignment, date functionality.

**Classes:** D2LDateProcessor

**Functions:** __init__, close, process_csv_file, set_assignment_due_date, set_assignment_start_date, setup_driver

**Globals:** _None_


**Local Imports:** _None_

**External Imports:** core.assignment_finder, core.browser_manager, core.date_editor, csv, logging, os, time


#### File I/O Summary

- Reads: _None_

- Writes: _None_


#### Threading & UI Bindings

- Threads: _None_

- UI Binds: _None_


#### Exception Paths

_No exception handlers detected._


---

### `d2l_playwright_processor.py`

**Intent:** Manages external processes for date operations.

**Classes:** D2LProcessor

**Functions:** __init__, _parse_time_str, _write_debug_report, automate_d2l, find_assignment_row, open_course, perform_date_updates, process_course, run_automation, set_date_in_dialog, update_due_date, update_start_date

**Globals:** COURSE_URLS, D2L_BASE_URL, LOGS_DIR, LOG_PATH, SHARED_BROWSER_DIR, action, course_code, csv_path, logger, processor, result, success


**Local Imports:** _None_

**External Imports:** asyncio, csv, datetime, json, logging, os, pandas, playwright.async_api, re, subprocess, sys, traceback


#### File I/O Summary

- Reads: _None_

- Writes: _None_


#### Threading & UI Bindings

- Threads: _None_

- UI Binds: _None_


#### Exception Paths

_No exception handlers detected._


---

### `D2L_Gui.py`

**Intent:** Creates and manages user interface components. Sets up various components.

**Classes:** D2LClassButtons, D2LClassButtonsGUI

**Functions:** __init__, async_navigation, browse_csv_file, cleanup_existing_processes, clear_login, exit_app, go_to_class, login_to_d2l, main, run, run_async_navigation, setup_browser, setup_gui, setup_logging, update_dates

**Globals:** _None_


**Local Imports:** _None_

**External Imports:** asyncio, d2l_date_processing, logging, os, pandas, playwright.async_api, shutil, subprocess, tempfile, threading, time, tkinter


#### File I/O Summary

- Reads: _None_

- Writes: _None_


#### Threading & UI Bindings

- Threads: run_async_navigation

- UI Binds: _None_


#### Exception Paths

_No exception handlers detected._


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
    "intent": "str"
  }
}
```


---

# 🧩 SHARED STATE TABLE
**Generated:** 2025-10-24 23:36:24

| File | Variable | Modified By | Read By |
|------|-----------|-------------|---------|
| D2L_Gui.py | `COMMAND_BINDS` | - | - |
| D2L_Gui.py | `GLOBALS` | - | - |
| D2L_Gui.py | `HOTKEYS` | - | - |
| D2L_Gui.py | `IMPORTS_LOCAL` | - | - |
| D2L_Gui.py | `INIT_SEQUENCE` | - | - |
| D2L_Gui.py | `IO_READS` | - | - |
| D2L_Gui.py | `IO_WRITES` | - | - |
| D2L_Gui.py | `STATE_VARS` | - | - |
| D2L_Gui.py | `TK_BINDS` | - | - |
| d2l_date_processing.py | `COMMAND_BINDS` | - | - |
| d2l_date_processing.py | `GLOBALS` | - | - |
| d2l_date_processing.py | `HOTKEYS` | - | - |
| d2l_date_processing.py | `IMPORTS_LOCAL` | - | - |
| d2l_date_processing.py | `INIT_SEQUENCE` | - | - |
| d2l_date_processing.py | `IO_READS` | - | - |
| d2l_date_processing.py | `IO_WRITES` | - | - |
| d2l_date_processing.py | `STATE_VARS` | - | - |
| d2l_date_processing.py | `THREAD_TARGETS` | - | - |
| d2l_date_processing.py | `TK_BINDS` | - | - |
| d2l_date_processing_new.py | `COMMAND_BINDS` | - | - |
| d2l_date_processing_new.py | `GLOBALS` | - | - |
| d2l_date_processing_new.py | `HOTKEYS` | - | - |
| d2l_date_processing_new.py | `IMPORTS_LOCAL` | - | - |
| d2l_date_processing_new.py | `INIT_SEQUENCE` | - | - |
| d2l_date_processing_new.py | `IO_READS` | - | - |
| d2l_date_processing_new.py | `IO_WRITES` | - | - |
| d2l_date_processing_new.py | `STATE_VARS` | - | - |
| d2l_date_processing_new.py | `THREAD_TARGETS` | - | - |
| d2l_date_processing_new.py | `TK_BINDS` | - | - |
| d2l_playwright_processor.py | `COMMAND_BINDS` | - | - |
| d2l_playwright_processor.py | `HOTKEYS` | - | - |
| d2l_playwright_processor.py | `IMPORTS_LOCAL` | - | - |
| d2l_playwright_processor.py | `IO_READS` | - | - |
| d2l_playwright_processor.py | `IO_WRITES` | - | - |
| d2l_playwright_processor.py | `THREAD_TARGETS` | - | - |
| d2l_playwright_processor.py | `TK_BINDS` | - | - |
| d2l_playwright_processor.py | `logger` | - | _parse_time_str +5 more, _write_debug_report, automate_d2l, open_course, process_course, run_automation |