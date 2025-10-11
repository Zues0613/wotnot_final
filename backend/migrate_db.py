"""
Database Migration Script
This script creates all tables in the Neon PostgreSQL database
"""
import asyncio
import sys
import io

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from wati.database import database
from wati.models import (
    User, 
    BroadcastList, 
    BroadcastAnalysis,
    Template,
    Contact, 
    Conversation, 
    Last_Conversation, 
    Integration, 
    Integration_credentials, 
    WooIntegration
)

async def create_tables():
    """Create all database tables"""
    try:
        print("Starting database migration...")
        print(f"Database URL: {database.SQLALCHEMY_DATABASE_URL.split('@')[1] if '@' in str(database.SQLALCHEMY_DATABASE_URL) else 'hidden'}")
        
        # Create all tables
        async with database.engine.begin() as conn:
            print("Creating tables...")
            await conn.run_sync(database.Base.metadata.create_all)
            print("✓ All tables created successfully!")
            
        # List created tables
        print("\nCreated tables:")
        for table_name in database.Base.metadata.tables.keys():
            print(f"  - {table_name}")
            
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Migration failed with error:")
        print(f"   {type(e).__name__}: {e}")
        sys.exit(1)
    finally:
        # Close the engine
        await database.engine.dispose()

async def drop_all_tables():
    """Drop all database tables (use with caution!)"""
    try:
        print("⚠️  WARNING: Dropping all tables...")
        async with database.engine.begin() as conn:
            await conn.run_sync(database.Base.metadata.drop_all)
            print("✓ All tables dropped successfully!")
    except Exception as e:
        print(f"❌ Failed to drop tables: {e}")
        sys.exit(1)
    finally:
        await database.engine.dispose()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Migration Tool')
    parser.add_argument(
        '--action',
        choices=['create', 'drop', 'recreate'],
        default='create',
        help='Migration action: create (default), drop, or recreate tables'
    )
    
    args = parser.parse_args()
    
    if args.action == 'create':
        asyncio.run(create_tables())
    elif args.action == 'drop':
        confirm = input("Are you sure you want to DROP all tables? Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            asyncio.run(drop_all_tables())
        else:
            print("Operation cancelled.")
    elif args.action == 'recreate':
        confirm = input("This will DROP and recreate all tables. All data will be lost! Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            asyncio.run(drop_all_tables())
            asyncio.run(create_tables())
        else:
            print("Operation cancelled.")

