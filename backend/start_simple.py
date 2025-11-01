#!/usr/bin/env python3
"""
WotNot Backend - Simple Startup Script for Render (No Redis dependency)
Starts only FastAPI Backend
"""

import os
import sys
from pathlib import Path

def main():
    """Simple startup function for production without Redis"""
    print("=" * 60)
    print("🚀 WotNot Backend - Simple Startup")
    print("=" * 60)
    print()
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Get port from environment (Render provides this)
    port = os.getenv('PORT', '8000')
    host = '0.0.0.0'  # Render requires binding to 0.0.0.0
    
    print(f"🌐 Starting FastAPI server on {host}:{port}")
    print("⚠️ Note: Redis features will be disabled")
    print("=" * 60)
    
    # Start FastAPI Backend
    cmd = f"{sys.executable} -m uvicorn wati.main:app --host {host} --port {port}"
    os.system(cmd)

if __name__ == "__main__":
    main()
