#!/usr/bin/env python3
import sys
import os

def view_logs():
    log_file = "backend/app.log"
    
    if not os.path.exists(log_file):
        print("No log file found. Run the application first.")
        return
    
    print("=== AUTO FORM FILLING AGENT LOGS ===\n")
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            
        # Show last 50 lines or all if less
        recent_lines = lines[-50:] if len(lines) > 50 else lines
        
        for line in recent_lines:
            print(line.strip())
            
    except Exception as e:
        print(f"Error reading log file: {e}")

if __name__ == "__main__":
    view_logs()