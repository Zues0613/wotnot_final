
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Fetch values
backend_url = os.getenv("BACKEND_URL")
database_url = os.getenv("DATABASE_URL")

# SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:Denmarks123$@localhost/wati_clone'


SQLALCHEMY_DATABASE_URL = database_url

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Denmarks123$@localhost/wati_clone'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()



# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import ssl

# Clean the database URL for asyncpg (remove psycopg2-specific parameters)
# asyncpg doesn't accept 'sslmode' and 'channel_binding' as URL parameters
if SQLALCHEMY_DATABASE_URL:
    # Remove psycopg2-specific SSL parameters from URL
    cleaned_url = SQLALCHEMY_DATABASE_URL.split('?')[0]
    
    # Configure SSL for asyncpg using connect_args
    connect_args = {
        "ssl": ssl.create_default_context(),
        "server_settings": {"jit": "off"}  # Disable JIT for better compatibility
    }
    
    # Only enable SQL logging in development mode
    environment = os.getenv("ENVIRONMENT", "prod").lower()
    enable_sql_logging = environment == "dev"
    
    engine = create_async_engine(
        cleaned_url, 
        echo=enable_sql_logging,  # Only log SQL in dev mode
        pool_recycle=120,
        pool_pre_ping=True,
        pool_size=5,  # Reduced from 30 to 5 for Render's 512MB memory limit
        max_overflow=10,  # Allow some overflow connections
        connect_args=connect_args
    )
else:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create a session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    
)

# Base class for declarative models
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

