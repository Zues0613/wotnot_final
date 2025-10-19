"""
Script to verify admin user exists in the database
"""
import asyncio
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from wati.database import database
from wati.models import User
from sqlalchemy.future import select

async def verify_admin():
    """Verify admin user exists"""
    try:
        print("Checking for admin user in database...\n")
        
        async with database.AsyncSessionLocal() as db:
            result = await db.execute(
                select(User).filter(User.email == "admin@wotnot.com")
            )
            admin = result.scalars().first()
            
            if admin:
                print("=" * 60)
                print("✅ ADMIN USER FOUND!")
                print("=" * 60)
                print(f"\nAdmin Details:")
                print(f"  User ID:      {admin.id}")
                print(f"  Username:     {admin.username}")
                print(f"  Email:        {admin.email}")
                print(f"  API Key:      {admin.api_key}")
                print(f"  Created At:   {admin.created_at}")
                print(f"  WABA ID:      {admin.WABAID}")
                print(f"  Phone ID:     {admin.Phone_id}")
                print(f"  Paid Amount:  ${admin.paid_amount}")
                print(f"\n🔐 Login Credentials:")
                print(f"  Email:        admin@wotnot.com")
                print(f"  Password:     admin123")
                print(f"\n🌐 Login URL:   http://127.0.0.1:8000/login")
                print("=" * 60)
            else:
                print("❌ Admin user not found in database!")
                
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        sys.exit(1)
    finally:
        await database.engine.dispose()

if __name__ == "__main__":
    asyncio.run(verify_admin())

