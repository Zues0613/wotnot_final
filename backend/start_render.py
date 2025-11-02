#!/usr/bin/env python3
"""
WotNot Backend - Render-optimized Startup Script
Starts FastAPI Backend directly (no subprocess wrapper)
"""

import os
import sys

def main():
    """Startup function optimized for Render"""
    print("=" * 60)
    print("🚀 WotNot Backend - Render Startup")
    print("=" * 60)
    print()
    
    # Get port from environment (Render provides this)
    port = os.getenv('PORT', '8000')
    host = '0.0.0.0'  # Render requires binding to 0.0.0.0
    
    print(f"🔍 Environment: {os.getenv('ENVIRONMENT', 'prod')}")
    print(f"🌐 Starting FastAPI server on {host}:{port}")
    print("=" * 60)
    print()
    
    # Start FastAPI Backend directly (this will block and keep the process alive)
    cmd = f"uvicorn wati.main:app --host {host} --port {port}"
    
    # Execute the command (this will block)
    os.execvp("uvicorn", ["uvicorn", "wati.main:app", "--host", host, "--port", port])

if __name__ == "__main__":
    main()

