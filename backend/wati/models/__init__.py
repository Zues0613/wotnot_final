# Import all models to ensure they are registered with Base.metadata
from .User import User
from .Broadcast import BroadcastList, BroadcastAnalysis, Template
from .Contacts import Contact
from .ChatBox import Conversation, Last_Conversation
from .Integration import Integration, Integration_credentials, WooIntegration

__all__ = [
    'User',
    'BroadcastList',
    'BroadcastAnalysis',
    'Template',
    'Contact',
    'Conversation',
    'Last_Conversation',
    'Integration',
    'Integration_credentials',
    'WooIntegration'
]

