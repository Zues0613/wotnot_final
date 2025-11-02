#!/usr/bin/env python3
"""
WotNot Backend - Complete Startup Script
Starts all required services: Redis, Dramatiq Worker, and FastAPI Backend
"""

import subprocess
import sys
import os
import time
import threading
import signal
from pathlib import Path

class ServiceManager:
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

def check_redis_installed():
    """Check if Redis is installed"""
    try:
        result = subprocess.run(["redis-server", "--version"], 
                              capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_redis_running():
    """Check if Redis is already running"""
    try:
        result = subprocess.run(["redis-cli", "ping"], 
                              capture_output=True, text=True, check=True)
        return "PONG" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_cloud_redis():
    """Check if cloud Redis (Upstash) is configured"""
    upstash_rest_url = os.getenv('UPSTASH_REDIS_REST_URL')
    upstash_rest_token = os.getenv('UPSTASH_REDIS_REST_TOKEN')
    redis_url = os.getenv('REDIS_URL')
    
    if upstash_rest_url and upstash_rest_token:
        print(f"✅ Upstash Redis configured: {upstash_rest_url[:30]}...")
        print("🔗 Using cloud Redis (no local installation needed)")
        return True
    elif redis_url and not redis_url.startswith('redis://localhost') and not redis_url.startswith('redis://127.0.0.1'):
        print(f"✅ Cloud Redis URL configured")
        print("🔗 Using cloud Redis (no local installation needed)")
        return True
    
    return False

def main():
    """Main startup function"""
    print("=" * 60)
    print("🚀 WotNot Backend - Complete Startup")
    print("=" * 60)
    print()
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Initialize service manager
    manager = ServiceManager()
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)
    
    # Check if cloud Redis (Upstash) is configured
    using_cloud_redis = False
    
    try:
        # Check if cloud Redis (Upstash) is configured - skip local Redis if so
        using_cloud_redis = check_cloud_redis()
        if using_cloud_redis:
            print("ℹ️  Skipping local Redis installation (using cloud Redis)")
        else:
            # Check if Redis is installed
            if not check_redis_installed():
                print("❌ Redis is not installed!")
                print("\n📋 Installation Instructions:")
                print("- Windows: Download from https://github.com/microsoftarchive/redis/releases")
                print("- macOS: brew install redis")
                print("- Linux: sudo apt-get install redis-server")
                print("- Docker: docker run -d -p 6379:6379 redis:alpine")
                print("\n💡 Or use cloud Redis (Upstash):")
                print("   Set UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN environment variables")
                sys.exit(1)
            
            # Check if Redis is already running
            if check_redis_running():
                print("✅ Redis is already running")
            else:
                # Start Redis
                manager.start_service("Redis", "redis-server")
                time.sleep(3)  # Wait for Redis to start
        
        # Start Dramatiq Worker
        dramatiq_cmd = f"{sys.executable} -m dramatiq wati.services.tasks"
        manager.start_service("Dramatiq Worker", dramatiq_cmd, delay=2)
        
        # Start FastAPI Backend
        # Use --reload only if RUNTIME_ENV is development
        reload_flag = "--reload" if os.getenv('RUNTIME_ENV', 'production') == 'development' else ""
        backend_cmd = f"{sys.executable} -m uvicorn wati.main:app --host 127.0.0.1 --port 8000 {reload_flag}".strip()
        manager.start_service("FastAPI Backend", backend_cmd, delay=2)
        
        print()
        print("=" * 60)
        print("✅ All services started successfully!")
        print("=" * 60)
        print()
        print("🌐 Services running:")
        if using_cloud_redis:
            print("- Redis: Cloud (Upstash)")
        else:
            print("- Redis: redis://127.0.0.1:6379")
        print("- Backend API: http://127.0.0.1:8000")
        print("- API Docs: http://127.0.0.1:8000/docs")
        print("- Dramatiq: Processing background tasks")
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
