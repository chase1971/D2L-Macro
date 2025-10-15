#!/usr/bin/env python3
"""
CLI wrapper for D2L Date Processing
Usage: python d2l_process_csv_cli.py <csv_file_path> <class_url>
"""

import sys
import json
from d2l_date_processing import D2LDateProcessor

def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False,
            "error": "Usage: python d2l_process_csv_cli.py <csv_file_path> <class_url>"
        }))
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    class_url = sys.argv[2]
    
    try:
        # Create processor instance
        processor = D2LDateProcessor()
        
        # Setup driver with existing session (user should already be logged in via browser)
        print("Setting up Chrome driver...", file=sys.stderr)
        if not processor.setup_driver(use_profile=True):
            print(json.dumps({
                "success": False,
                "error": "Failed to setup Chrome driver"
            }))
            sys.exit(1)
        
        # Navigate to class URL
        print(f"Navigating to class URL: {class_url}", file=sys.stderr)
        processor.driver.get(class_url)
        
        # Give time for page to load
        import time
        time.sleep(3)
        
        # Process CSV file
        print(f"Processing CSV file: {csv_file_path}", file=sys.stderr)
        processed, errors = processor.process_csv_file(csv_file_path)
        
        # Return result as JSON
        result = {
            "success": True,
            "processed": processed,
            "errors": errors,
            "message": f"Processed {processed} assignments with {errors} errors"
        }
        
        print(json.dumps(result))
        
    except FileNotFoundError:
        print(json.dumps({
            "success": False,
            "error": f"CSV file not found: {csv_file_path}"
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))
        sys.exit(1)
    finally:
        # Cleanup
        try:
            if hasattr(processor, 'driver') and processor.driver:
                processor.driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()

