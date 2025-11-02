from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from .database import database
from .routes import user, broadcast, contacts, auth, woocommerce, integration, wallet,analytics, message_generator
from .services import dramatiq_router
from . import oauth2
from wati.models.ChatBox import Last_Conversation
from .models import ChatBox
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional

# Import AI message template components
from .message_template_ai import MessageTemplateGenerator, ComponentConfig

# Pydantic models for AI endpoint
class MessageRequest(BaseModel):
    prompt: str
    tone: str = "informal"
    length: str = "medium"
    placeholders: str = ""
    audience: str = ""

class MessageResponse(BaseModel):
    success: bool
    message: str
    source: str
    error: Optional[str] = None
    prompt: str
    length: str
    placeholders: str
    audience: str
    metadata: dict = {}

# Create FastAPI app
app = FastAPI()
scheduler = AsyncIOScheduler()

# Initialize AI Message Generator
ai_generator = None

# Models creation
async def create_db_and_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

scheduler_started = False

@app.on_event("startup")
async def startup_event():
    global ai_generator, scheduler_started
    
    # Create database tables
    await create_db_and_tables()
    
    # Initialize AI generator
    try:
        config = ComponentConfig.from_env()
        ai_generator = MessageTemplateGenerator(config)
        await ai_generator.initialize()
        print("✓ AI Message Generator initialized successfully")
    except Exception as e:
        print(f"⚠ AI Message Generator initialization failed: {e}")
        print("  (AI features will be disabled, but app will continue)")
    
    # Start scheduler for closing expired chats
    # Changed to run every 10 minutes instead of 1 minute to reduce DB/Redis requests
    if not scheduler_started:
        scheduler.add_job(close_expired_chats, 'interval', minutes=10)
        scheduler.start()
        scheduler_started = True
        print("✓ Scheduler started (runs every 10 minutes)")

@app.on_event("shutdown")
async def shutdown_event():
    global ai_generator, scheduler_started
    
    # Cleanup AI generator
    if ai_generator:
        await ai_generator.cleanup()
    
    # Shutdown scheduler
    if scheduler_started:
        scheduler.shutdown(wait=False)
        scheduler_started = False
        print("✓ Scheduler shut down")

async def close_expired_chats() -> None:
    """Close chats that have been inactive for more than 24 hours."""
    try:
        async for session in database.get_db():
            now = datetime.now()  
            result = await session.execute(
                select(ChatBox.Last_Conversation).where(
                    ChatBox.Last_Conversation.active == True,
                    now - ChatBox.Last_Conversation.last_chat_time > timedelta(minutes=1440)
                )
            )
            expired_conversations = result.scalars().all()
            for conversation in expired_conversations:
                conversation.active = False
            await session.commit()
            print(f"Successfully closed {len(expired_conversations)} expired chats.")
            break
    except Exception as e:
        print(f"Error in close_expired_chats: {e}")

# CORS middleware configuration (MUST be added BEFORE routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Template Generation Endpoint
@app.post("/api/templates/generate", response_model=MessageResponse, tags=["AI Templates"])
async def generate_template_api(request_data: MessageRequest):
    """Generate message template using AI (DeepSeek R1 via OpenRouter)"""
    global ai_generator
    
    if not ai_generator:
        return MessageResponse(
            success=False,
            message="",
            source="error",
            error="AI Generator not initialized. Please check OPENROUTER_API_KEY in .env",
            prompt=request_data.prompt,
            length=request_data.length,
            placeholders=request_data.placeholders,
            audience=request_data.audience,
            metadata={}
        )
    
    try:
        result = await ai_generator.generate(
            prompt=request_data.prompt,
            tone=request_data.tone,
            length=request_data.length,
            placeholders=request_data.placeholders,
            audience=request_data.audience
        )
        
        return MessageResponse(
            success=result["source"] != "error",
            message=result["message"],
            source=result["source"],
            error=result["error"],
            prompt=request_data.prompt,
            length=request_data.length,
            placeholders=request_data.placeholders,
            audience=request_data.audience,
            metadata=result["metadata"]
        )
    except Exception as e:
        return MessageResponse(
            success=False,
            message="",
            source="error",
            error=str(e),
            prompt=request_data.prompt,
            length=request_data.length,
            placeholders=request_data.placeholders,
            audience=request_data.audience,
            metadata={}
        )

# Adding the routes
app.include_router(broadcast.router)
app.include_router(contacts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(oauth2.router)
app.include_router(dramatiq_router.router)
app.include_router(woocommerce.router)
app.include_router(integration.router)
app.include_router(analytics.router)
app.include_router(message_generator.router)

# Print all registered routes for debugging
from fastapi.routing import APIRoute
print("\n" + "="*50)
print("REGISTERED API ROUTES:")
print("="*50)
for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"{route.path} -> {route.methods}")
print("="*50 + "\n")

# Scheduler is already initialized and events are handled above
