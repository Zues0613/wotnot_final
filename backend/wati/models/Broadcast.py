from ..database import database
from sqlalchemy import Integer,Column,String,ARRAY,Boolean,JSON
from . import User
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, func


# broadcast List
class BroadcastList(database.Base):
    __tablename__="BroadcastList"
    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer,ForeignKey("Users.id")) # Foreign key to Users table
    name = Column(String)
    type = Column(String, nullable=True)
    template = Column(String)
    contacts = Column(ARRAY(String))
    # contacts = Column(JSON, nullable=False)
    success = Column(Integer)
    failed = Column(Integer)
    status = Column(String)
    scheduled_time = Column(TIMESTAMP, nullable=True)  # Allows NULL for immediate broadcasts
    task_id = Column(String, nullable=True)  # Stores the task ID for scheduled broadcasts
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    

class BroadcastAnalysis(database.Base):
    __tablename__="BroadcastAnalysis"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer,ForeignKey("Users.id"))
    broadcast_id = Column(Integer,ForeignKey("BroadcastList.id"))
    status=Column(String)
    message_id = Column(String,unique=True)
    phone_no=Column(String)
    contact_name=Column(String)
    read=Column(Boolean,nullable=True)
    delivered=Column(Boolean,nullable=True)
    sent=Column(Boolean,nullable=True)
    replied=Column(Boolean,nullable=True)
    error_reason=Column(String,nullable=True)


class Template(database.Base):
    __tablename__="Templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))  # Foreign key to Users table
    template_id = Column(String, nullable=False)  # WhatsApp's template ID
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)
    sub_category = Column(String, nullable=True)
    language = Column(String, nullable=False)
    status = Column(String, nullable=False)  # e.g., 'PENDING', 'APPROVED', 'REJECTED'
    components = Column(JSON, nullable=False)  # Store template components as JSON
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete flag
    deleted_at = Column(TIMESTAMP, nullable=True)  # When template was deleted
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())