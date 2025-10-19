#!/usr/bin/env python3
"""
Dramatiq Worker Startup Script
Starts the Dramatiq worker for background tasks
"""

import subprocess
import sys
import os
from pathlib import Path

def start_dramatiq():
    """Start the Dramatiq worker"""
    print("⚙️ Starting Dramatiq Worker...")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    try:
        # Start the Dramatiq worker
        cmd = [
            sys.executable, "-m", "dramatiq", 
            "wati.services.dramatiq_router"
        ]
        
        print(f"Running: {' '.join(cmd)}")
        print("Dramatiq worker is processing background tasks...")
        print("Press Ctrl+C to stop the worker")
        print("=" * 50)
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Dramatiq worker stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Dramatiq worker: {e}")
        print("Make sure Redis is running!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_dramatiq()
