"""
Base Tool Class
Abstract base for all API tools
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseTool(ABC):
    """Abstract base class for all tools"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for LLM to understand when to use it"""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters
        
        Returns:
            Dict with 'success', 'data', and optional 'error' keys
        """
        pass
    
    def get_tool_info(self) -> Dict[str, str]:
        """Get tool information for planner"""
        return {
            "name": self.name,
            "description": self.description
        }
