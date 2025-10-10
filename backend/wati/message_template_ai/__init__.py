"""Message Template AI Generator Component."""

from .core import MessageTemplateGenerator
from .config import ComponentConfig
from .router import create_router

__all__ = ['MessageTemplateGenerator', 'ComponentConfig', 'create_router']

