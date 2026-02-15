"""Custom exceptions for the Invoice Agent"""

class AgentException(Exception):
    """Base exception for all agent errors"""
    pass

class LLMError(AgentException):
    """Error related to LLM operations"""
    pass

class MCPError(AgentException):
    """Error related to MCP operations"""
    pass

class VoiceInputError(AgentException):
    """Error related to voice input"""
    pass

class ValidationError(AgentException):
    """Error related to input validation"""
    pass

class ConfigurationError(AgentException):
    """Error related to configuration"""
    pass
