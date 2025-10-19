#!/usr/bin/env python3
"""
Redis Server Startup Script
Starts Redis server for Dramatiq message broker
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def check_redis_installed():
    """Check if Redis is installed"""
    try:
        subprocess.run(["redis-server", "--version"], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def start_redis():
    """Start Redis server"""
    print("🔴 Starting Redis Server...")
    print("=" * 50)
    
    # Check if Redis is installed
    if not check_redis_installed():
        print("❌ Redis is not installed!")
        print("\n📋 Installation Instructions:")
        print("- Windows: Download from https://github.com/microsoftarchive/redis/releases")
        print("- macOS: brew install redis")
        print("- Linux: sudo apt-get install redis-server")
        print("\nOr use Docker: docker run -d -p 6379:6379 redis:alpine")
        sys.exit(1)
    
    try:
        print("Starting Redis server on port 6379...")
        print("Redis will be available at: redis://127.0.0.1:6379")
        print("Press Ctrl+C to stop Redis")
        print("=" * 50)
        
        # Start Redis server
        subprocess.run(["redis-server"], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Redis server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Redis server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_redis()
