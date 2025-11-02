#!/usr/bin/env python3
"""
WotNot Backend - Production Startup Script for Render
Starts FastAPI Backend and Dramatiq Worker (Redis provided by Render)
"""

import subprocess
import sys
import os
import time
import threading
import signal
from pathlib import Path

class ProductionServiceManager:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_service(self, name, cmd, delay=0):
        """Start a service with optional delay"""
        if delay > 0:
            time.sleep(delay)
            
        print(f"🚀 Starting {name}...")
        try:
            process = subprocess.Popen(cmd, shell=True)
            self.processes.append((name, process))
            print(f"✅ {name} started (PID: {process.pid})")
            return process
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
            return None
    
    def stop_all_services(self):
        """Stop all running services"""
        print("\n🛑 Stopping all services...")
        self.running = False
        
        for name, process in self.processes:
            try:
                print(f"Stopping {name}...")
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                print(f"⚠️ Force killing {name}...")
                process.kill()
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n🛑 Received interrupt signal...")
        self.stop_all_services()
        sys.exit(0)

def check_redis_connection():
    """Check if Redis is accessible via environment variable"""
    # Check environment variable
    environment = os.getenv("ENVIRONMENT", "prod").lower()
    env_raw = os.getenv("ENVIRONMENT", "NOT_SET")
    print(f"🔍 Environment: '{env_raw}' (normalized: '{environment}')")
    
    # In production mode, check for cloud Redis
    upstash_rest_url = os.getenv('UPSTASH_REDIS_REST_URL')
    upstash_rest_token = os.getenv('UPSTASH_REDIS_REST_TOKEN')
    
    # Check for standard Redis URL
    redis_url = os.getenv('REDIS_URL')
    
    # Debug: Print what we found
    print(f"🔍 Checking for cloud Redis...")
    print(f"   UPSTASH_REDIS_REST_URL: {'✅ Found' if upstash_rest_url else '❌ Not set'}")
    print(f"   UPSTASH_REDIS_REST_TOKEN: {'✅ Found' if upstash_rest_token else '❌ Not set'}")
    print(f"   REDIS_URL: {'✅ Found' if redis_url else '❌ Not set'}")
    
    if upstash_rest_url and upstash_rest_token:
        print(f"✅ Upstash Redis REST URL found: {upstash_rest_url[:30]}...")
        print("🔗 Using Upstash Redis for background tasks")
        return True
    elif redis_url:
        print(f"✅ Redis URL found: {redis_url[:20]}...")
        print("🔗 Using Redis for background tasks")
        return True
    else:
        print("⚠️ Redis connection not configured")
        print("📋 Add one of the following:")
        print("   Option 1 (Upstash): UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN")
        print("   Option 2 (Standard): REDIS_URL")
        print("📋 Get Upstash credentials from: https://console.upstash.com/")
        return False

def main():
    """Main startup function for production"""
    print("=" * 60)
    print("🚀 WotNot Backend - Production Startup")
    print("=" * 60)
    print()
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Initialize service manager
    manager = ProductionServiceManager()
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)
    
    try:
        # Check Redis connection
        if not check_redis_connection():
            print("❌ Redis connection not available!")
            print("\n📋 To fix this:")
            print("Option 1 - Use Upstash Redis (Recommended):")
            print("1. Go to https://console.upstash.com/")
            print("2. Create a Redis database")
            print("3. Copy REST URL and REST Token")
            print("4. Add UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN to environment variables")
            print("\nOption 2 - Use Standard Redis:")
            print("1. Add REDIS_URL environment variable")
            sys.exit(1)
        
        # Get port from environment (Render provides this)
        port = os.getenv('PORT', '8000')
        host = '0.0.0.0'  # Render requires binding to 0.0.0.0
        
        # Start Dramatiq Worker in background
        dramatiq_cmd = f"{sys.executable} -m dramatiq wati.services.tasks"
        manager.start_service("Dramatiq Worker", dramatiq_cmd, delay=2)
        
        # Start FastAPI Backend (main process)
        # Production: No --reload flag (reduces unnecessary file watching and Redis requests)
        backend_cmd = f"{sys.executable} -m uvicorn wati.main:app --host {host} --port {port}"
        manager.start_service("FastAPI Backend", backend_cmd, delay=2)
        
        print()
        print("=" * 60)
        print("✅ All services started successfully!")
        print("=" * 60)
        print()
        print("🌐 Services running:")
        print(f"- Backend API: http://{host}:{port}")
        print(f"- API Docs: http://{host}:{port}/docs")
        print("- Dramatiq: Processing background tasks")
        print("- Redis: Managed by Render")
        print()
        print("Press Ctrl+C to stop all services")
        print("=" * 60)
        
        # Keep the main thread alive
        while manager.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Received interrupt signal...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        manager.stop_all_services()

if __name__ == "__main__":
    main()
