"""
Script to create admin user in the database
"""
import asyncio
import sys
import io
import secrets

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from wati.database import database
from wati.models import User
from wati import hashing
from sqlalchemy.future import select

async def create_admin_user():
    """Create admin user with predefined credentials"""
    try:
        print("Connecting to database...")
        
        # Admin credentials
        admin_email = "admin@wotnot.com"
        admin_password = "admin123"
        admin_username = "Admin"
        
        # Check if admin user already exists
        async with database.AsyncSessionLocal() as db:
            result = await db.execute(
                select(User).filter(User.email == admin_email)
            )
            existing_admin = result.scalars().first()
            
            if existing_admin:
                print(f"⚠️  Admin user already exists with email: {admin_email}")
                print(f"   User ID: {existing_admin.id}")
                print(f"   Username: {existing_admin.username}")
                
                # Ask if user wants to update password
                update = input("\nDo you want to update the admin password? (yes/no): ")
                if update.lower() == 'yes':
                    existing_admin.password_hash = hashing.Hash.bcrypt(admin_password)
                    await db.commit()
                    print("✅ Admin password updated successfully!")
                else:
                    print("❌ Operation cancelled.")
                return
            
            # Generate API key
            api_key = secrets.token_hex(32)
            
            # Create admin user
            admin_user = User(
                username=admin_username,
                email=admin_email,
                password_hash=hashing.Hash.bcrypt(admin_password),
                api_key=api_key
            )
            
            db.add(admin_user)
            await db.commit()
            await db.refresh(admin_user)
            
            print("\n✅ Admin user created successfully!")
            print(f"\n📋 Admin Details:")
            print(f"   Email: {admin_user.email}")
            print(f"   Username: {admin_user.username}")
            print(f"   Password: {admin_password}")
            print(f"   User ID: {admin_user.id}")
            print(f"   API Key: {admin_user.api_key}")
            print(f"\n🔐 Login URL: http://127.0.0.1:8000/login")
            
    except Exception as e:
        print(f"\n❌ Error creating admin user:")
        print(f"   {type(e).__name__}: {e}")
        sys.exit(1)
    finally:
        # Close the engine
        await database.engine.dispose()

if __name__ == "__main__":
    print("=" * 60)
    print("         Creating Admin User for WotNot")
    print("=" * 60)
    asyncio.run(create_admin_user())

