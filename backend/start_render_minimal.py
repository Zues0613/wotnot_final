#!/usr/bin/env python3
"""
WotNot Backend - Minimal Render Startup Script
Just starts uvicorn directly
"""

import os
import subprocess

def main():
    port = os.getenv('PORT', '8000')
    host = '0.0.0.0'
    
    print(f"Starting on {host}:{port}")
    
    # Replace current process with uvicorn
    subprocess.run([
        "uvicorn", "wati.main:app",
        "--host", host,
        "--port", port
    ])

if __name__ == "__main__":
    main()

