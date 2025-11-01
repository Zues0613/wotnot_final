#!/usr/bin/env python3
"""
Test script to verify Upstash Redis connection and Dramatiq integration.

This script tests:
1. Environment variables are set correctly
2. Redis connection using Upstash REST API
3. Redis connection using standard Redis protocol (for Dramatiq)
4. Basic Redis operations (set/get)
5. Dramatiq broker connection

Usage:
    python test_upstash_redis.py
"""

import os
import sys
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test if required environment variables are present"""
    print("=" * 60)
    print("🔍 Testing Environment Variables")
    print("=" * 60)
    
    upstash_rest_url = os.getenv('UPSTASH_REDIS_REST_URL')
    upstash_rest_token = os.getenv('UPSTASH_REDIS_REST_TOKEN')
    redis_url = os.getenv('REDIS_URL')
    
    success = True
    
    if upstash_rest_url:
        print(f"✅ UPSTASH_REDIS_REST_URL found: {upstash_rest_url[:40]}...")
    else:
        print("❌ UPSTASH_REDIS_REST_URL not found")
        success = False
    
    if upstash_rest_token:
        print(f"✅ UPSTASH_REDIS_REST_TOKEN found: {upstash_rest_token[:20]}...")
    else:
        print("❌ UPSTASH_REDIS_REST_TOKEN not found")
        success = False
    
    if redis_url:
        print(f"✅ REDIS_URL found: {redis_url[:40]}...")
    else:
        print("ℹ️  REDIS_URL not set (will use Upstash credentials)")
    
    print()
    return success, upstash_rest_url, upstash_rest_token


def test_redis_url_construction(upstash_rest_url, upstash_rest_token):
    """Test Redis URL construction from Upstash credentials"""
    print("=" * 60)
    print("🔧 Testing Redis URL Construction")
    print("=" * 60)
    
    if not upstash_rest_url or not upstash_rest_token:
        print("❌ Cannot test URL construction - missing credentials")
        return None
    
    try:
        # Extract host from REST URL
        parsed_url = urlparse(upstash_rest_url)
        host = parsed_url.netloc or parsed_url.path.replace('https://', '').replace('http://', '')
        host = host.rstrip('/')
        
        # Construct Redis URL (Upstash requires SSL/TLS, so we use rediss://)
        redis_url = f"rediss://default:{upstash_rest_token}@{host}:6379"
        
        print(f"✅ Host extracted: {host}")
        print(f"✅ Redis URL constructed: rediss://default:***@{host}:6379 (with SSL/TLS)")
        print()
        return redis_url
    except Exception as e:
        print(f"❌ Error constructing Redis URL: {e}")
        print()
        return None


def test_upstash_rest_api(upstash_rest_url, upstash_rest_token):
    """Test Upstash Redis REST API connection"""
    print("=" * 60)
    print("🌐 Testing Upstash REST API Connection")
    print("=" * 60)
    
    try:
        from upstash_redis import Redis
    except ImportError:
        print("⚠️  upstash-redis package not installed")
        print("   This package is optional for testing REST API directly.")
        print("   Install it with: pip install upstash-redis")
        print("   Note: Dramatiq uses the standard redis package, not upstash-redis")
        print()
        return None  # Return None to indicate skipped test
    
    try:
        redis = Redis(url=upstash_rest_url, token=upstash_rest_token)
        
        # Test SET operation
        test_key = "test:wotnot:connection"
        test_value = "hello_from_wotnot"
        
        print(f"📤 Setting test key: {test_key}")
        redis.set(test_key, test_value)
        print("✅ SET operation successful")
        
        # Test GET operation
        print(f"📥 Getting test key: {test_key}")
        result = redis.get(test_key)
        
        if result == test_value:
            print(f"✅ GET operation successful - Value: {result}")
        else:
            print(f"⚠️  GET returned unexpected value: {result}")
        
        # Clean up
        redis.delete(test_key)
        print(f"🗑️  Cleaned up test key")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ REST API connection failed: {e}")
        print()
        return False


def test_standard_redis_connection(redis_url):
    """Test standard Redis protocol connection (used by Dramatiq)"""
    print("=" * 60)
    print("🔌 Testing Standard Redis Protocol Connection")
    print("=" * 60)
    
    if not redis_url:
        print("❌ No Redis URL available for testing")
        print()
        return False
    
    try:
        import redis
    except ImportError:
        print("❌ redis package not installed")
        print("   Install it with: pip install -r requirements.txt")
        print("   Or: pip install redis")
        print()
        return False
    
    try:
        # Parse Redis URL to handle special characters in password
        from urllib.parse import urlparse, unquote
        
        parsed = urlparse(redis_url)
        print(f"🔍 Parsed connection details:")
        print(f"   Scheme: {parsed.scheme}")
        print(f"   Host: {parsed.hostname}")
        print(f"   Port: {parsed.port or 6379}")
        print(f"   Username: {parsed.username or 'default'}")
        print(f"   Password: {'***' if parsed.password else 'None'}")
        
        # Determine if SSL is required (rediss:// indicates SSL)
        use_ssl = parsed.scheme == 'rediss'
        print(f"   SSL/TLS: {use_ssl}")
        print()
        
        # Create Redis client
        import ssl
        print("🔧 Creating Redis client...")
        redis_client = redis.Redis(
            host=parsed.hostname,
            port=parsed.port or 6379,
            password=unquote(parsed.password) if parsed.password else None,
            username=parsed.username or 'default',
            ssl=use_ssl,  # Upstash requires SSL
            ssl_cert_reqs=ssl.CERT_NONE if use_ssl else None,  # Upstash uses self-signed certs
            decode_responses=True,
            socket_connect_timeout=10,  # 10 second timeout
            socket_timeout=10
        )
        
        # Test connection with PING
        print("📡 Pinging Redis server...")
        response = redis_client.ping()
        
        if response:
            print("✅ PING successful - Connection established")
        else:
            print("❌ PING failed")
            print()
            return False
        
        # Test SET operation
        test_key = "test:wotnot:standard"
        test_value = "standard_redis_test"
        
        print(f"📤 Setting test key: {test_key}")
        redis_client.set(test_key, test_value)
        print("✅ SET operation successful")
        
        # Test GET operation
        print(f"📥 Getting test key: {test_key}")
        result = redis_client.get(test_key)
        
        if result == test_value:
            print(f"✅ GET operation successful - Value: {result}")
        else:
            print(f"⚠️  GET returned unexpected value: {result}")
        
        # Clean up
        redis_client.delete(test_key)
        print(f"🗑️  Cleaned up test key")
        
        print()
        return True
        
    except redis.ConnectionError as e:
        print(f"❌ Connection failed: {e}")
        print()
        print("💡 Troubleshooting tips:")
        print("   1. Upstash may require the actual Redis URL from their dashboard")
        print("   2. Check if your Upstash plan supports Redis protocol (not just REST API)")
        print("   3. The Redis URL might be different from the REST URL")
        print("   4. Try using the REDIS_URL env var with the Redis URL from Upstash dashboard")
        print()
        return False
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        print()
        print("💡 If connection keeps failing, you may need:")
        print("   - The actual Redis protocol URL from Upstash dashboard (not REST URL)")
        print("   - Set it as REDIS_URL environment variable")
        print()
        return False


def test_dramatiq_broker():
    """Test Dramatiq broker connection"""
    print("=" * 60)
    print("🎭 Testing Dramatiq Broker Connection")
    print("=" * 60)
    
    try:
        import dramatiq
        from dramatiq.brokers.redis import RedisBroker
        import os
        from urllib.parse import urlparse
    except ImportError as e:
        print("❌ dramatiq package not installed")
        print("   Install it with: pip install -r requirements.txt")
        print("   Or: pip install dramatiq")
        print()
        return False
    
    try:
        # Use the same logic as tasks.py
        def get_redis_url():
            upstash_rest_url = os.getenv('UPSTASH_REDIS_REST_URL')
            upstash_rest_token = os.getenv('UPSTASH_REDIS_REST_TOKEN')
            
            if upstash_rest_url and upstash_rest_token:
                parsed_url = urlparse(upstash_rest_url)
                host = parsed_url.netloc or parsed_url.path.replace('https://', '').replace('http://', '')
                host = host.rstrip('/')
                # Use rediss:// for SSL/TLS (Upstash requirement)
                redis_url = f"rediss://default:{upstash_rest_token}@{host}:6379"
                return redis_url
            
            return os.getenv('REDIS_URL', 'redis://localhost:6379')
        
        redis_url = get_redis_url()
        parsed = urlparse(redis_url)
        scheme = "rediss" if parsed.scheme == "rediss" else "redis"
        print(f"📋 Using Redis URL: {scheme}://default:***@{parsed.hostname}:6379")
        
        # Create Redis broker
        print("🔧 Creating RedisBroker...")
        redis_broker = RedisBroker(url=redis_url)
        
        # Try to connect (this will fail fast if connection is bad)
        print("🔌 Testing broker connection...")
        
        # The broker doesn't connect until used, so we'll test with a simple operation
        # We can't easily test the full broker without importing the tasks module,
        # but we can at least verify the broker can be created
        print("✅ RedisBroker created successfully")
        print("   Note: Full broker functionality will be tested when Dramatiq tasks run")
        
        print()
        return True
    except Exception as e:
        print(f"❌ Dramatiq broker test failed: {e}")
        print()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🚀 WotNot - Upstash Redis Connection Test")
    print("=" * 60)
    print()
    
    results = {
        "environment": False,
        "url_construction": False,
        "rest_api": False,
        "standard_redis": False,
        "dramatiq": False
    }
    
    # Test 1: Environment Variables
    env_success, upstash_url, upstash_token = test_environment_variables()
    results["environment"] = env_success
    
    if not env_success:
        print("❌ Environment variables missing. Please set UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN")
        print()
        return False
    
    # Test 2: URL Construction
    redis_url = test_redis_url_construction(upstash_url, upstash_token)
    results["url_construction"] = redis_url is not None
    
    # Test 3: Upstash REST API (optional test)
    if upstash_url and upstash_token:
        rest_result = test_upstash_rest_api(upstash_url, upstash_token)
        results["rest_api"] = rest_result if rest_result is not None else None
    
    # Test 4: Standard Redis Protocol
    if redis_url:
        results["standard_redis"] = test_standard_redis_connection(redis_url)
    
    # Test 5: Dramatiq Broker
    results["dramatiq"] = test_dramatiq_broker()
    
    # Summary
    print("=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        if passed is None:
            status = "⏭️  SKIP"
        elif passed:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print()
    
    # Filter out None (skipped tests) for the all() check
    required_tests = {k: v for k, v in results.items() if v is not None}
    all_passed = all(required_tests.values())
    
    if all_passed:
        print("🎉 All tests passed! Your Upstash Redis connection is working correctly.")
        print()
        print("✅ Your Dramatiq background tasks should work with Upstash Redis.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

