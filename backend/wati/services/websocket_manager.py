"""
WebSocket Manager for Real-time Updates
Handles WebSocket connections and broadcasts updates to connected clients
"""
import json
import asyncio
from typing import Dict, Set, Any
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        # Store active connections: {user_id: {websocket, db_session}}
        self.active_connections: Dict[int, Dict[str, Any]] = {}
        # Store conversations connections: {contact_number: {user_id: websocket}}
        self.conversation_connections: Dict[str, Dict[int, WebSocket]] = {}
        self.lock = asyncio.Lock()
    
    async def connect_active_conversations(self, websocket: WebSocket, user_id: int, db: AsyncSession):
        """Connect a client for active conversations updates"""
        await websocket.accept()
        async with self.lock:
            self.active_connections[user_id] = {
                'websocket': websocket,
                'db': db
            }
        print(f"✅ WebSocket connected for active conversations (user_id: {user_id})")
    
    async def connect_conversation(self, websocket: WebSocket, user_id: int, contact_number: str):
        """Connect a client for specific conversation updates"""
        await websocket.accept()
        async with self.lock:
            if contact_number not in self.conversation_connections:
                self.conversation_connections[contact_number] = {}
            self.conversation_connections[contact_number][user_id] = websocket
        print(f"✅ WebSocket connected for conversation {contact_number} (user_id: {user_id})")
    
    async def disconnect_active_conversations(self, user_id: int):
        """Disconnect a client from active conversations"""
        async with self.lock:
            if user_id in self.active_connections:
                connection = self.active_connections.pop(user_id)
                try:
                    await connection['websocket'].close()
                except:
                    pass
                print(f"❌ WebSocket disconnected for active conversations (user_id: {user_id})")
    
    async def disconnect_conversation(self, user_id: int, contact_number: str):
        """Disconnect a client from conversation"""
        async with self.lock:
            if contact_number in self.conversation_connections:
                if user_id in self.conversation_connections[contact_number]:
                    websocket = self.conversation_connections[contact_number].pop(user_id)
                    try:
                        await websocket.close()
                    except:
                        pass
                    print(f"❌ WebSocket disconnected from conversation {contact_number} (user_id: {user_id})")
                
                # Clean up empty conversation dicts
                if not self.conversation_connections[contact_number]:
                    del self.conversation_connections[contact_number]
    
    async def broadcast_active_conversations_update(self, user_id: int, data: dict):
        """Broadcast active conversations update to specific user (event-driven, only when update occurs)"""
        async with self.lock:
            if user_id in self.active_connections:
                websocket = self.active_connections[user_id]['websocket']
                try:
                    # Send update immediately (no polling, event-driven)
                    await websocket.send_json(data)
                    return True
                except Exception as e:
                    print(f"⚠️ Error sending update to user {user_id}: {e}")
                    # Connection might be dead, clean it up
                    try:
                        await self.disconnect_active_conversations(user_id)
                    except:
                        pass
                    return False
        return False
    
    async def broadcast_conversation_update(self, contact_number: str, data: dict):
        """Broadcast conversation update to all users watching this conversation (event-driven, only when update occurs)"""
        async with self.lock:
            if contact_number in self.conversation_connections:
                disconnected_users = []
                for user_id, websocket in self.conversation_connections[contact_number].items():
                    try:
                        # Send update immediately (no polling, event-driven)
                        await websocket.send_json(data)
                    except Exception as e:
                        print(f"⚠️ Error sending update to user {user_id} for conversation {contact_number}: {e}")
                        disconnected_users.append(user_id)
                
                # Clean up disconnected users
                for user_id in disconnected_users:
                    try:
                        await self.disconnect_conversation(user_id, contact_number)
                    except:
                        pass
                
                return len(self.conversation_connections.get(contact_number, {})) > 0
        return False
    
    async def broadcast_to_all_active_users(self, data: dict):
        """Broadcast to all users watching active conversations"""
        async with self.lock:
            disconnected_users = []
            for user_id, connection in self.active_connections.items():
                try:
                    await connection['websocket'].send_json(data)
                except Exception as e:
                    print(f"⚠️ Error broadcasting to user {user_id}: {e}")
                    disconnected_users.append(user_id)
            
            # Clean up disconnected users
            for user_id in disconnected_users:
                await self.disconnect_active_conversations(user_id)
    
    def get_active_user_count(self) -> int:
        """Get count of active connections"""
        return len(self.active_connections)
    
    def get_conversation_watchers(self, contact_number: str) -> int:
        """Get count of users watching a specific conversation"""
        return len(self.conversation_connections.get(contact_number, {}))

# Global WebSocket manager instance
manager = ConnectionManager()

