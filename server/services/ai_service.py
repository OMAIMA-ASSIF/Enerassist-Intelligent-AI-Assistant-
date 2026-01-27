"""
AI Service Layer - Abstraction for AI model integration
Provides a clean interface to interact with the chatbot AI model
"""
import sys
import os
from typing import List, Dict, AsyncGenerator
from datetime import datetime

# Add the ai directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai"))

from ai.chatbot import get_chatbot_chain
from server.models import MessageBase


class AIService:
    """
    Service layer for AI model integration
    Handles all AI-related operations in a pluggable, testable manner
    """
    
    def __init__(self):
        """Initialize the AI service with the chatbot chain"""
        self._chain = None
    
    def _get_chain(self):
        """Lazy initialization of the chatbot chain"""
        if self._chain is None:
            self._chain = get_chatbot_chain()
        return self._chain
    
    async def generate_response(
        self,
        user_message: str,
        conversation_id: str,
        chat_history: List[MessageBase]
    ) -> str:
        """
        Generate AI response for a user message
        
        Args:
            user_message: The user's input message
            conversation_id: Unique conversation identifier (used as session_id)
            chat_history: Previous messages in the conversation
            
        Returns:
            AI-generated response text
        """
        try:
            chain = self._get_chain()
            
            # Configure session for conversation context
            config = {
                "configurable": {
                    "session_id": conversation_id
                }
            }
            
            # Stream the response and collect chunks
            response_chunks = []
            
            async for chunk in self._stream_response(
                chain=chain,
                user_message=user_message,
                config=config
            ):
                response_chunks.append(chunk)
            
            # Join all chunks to get complete response
            complete_response = "".join(response_chunks)
            
            return complete_response
            
        except Exception as e:
            print(f"❌ AI Service Error: {str(e)}")
            raise AIServiceException(f"Failed to generate AI response: {str(e)}")
    
    async def _stream_response(
        self,
        chain,
        user_message: str,
        config: Dict
    ) -> AsyncGenerator[str, None]:
        """
        Stream AI response chunks
        
        Note: This is a synchronous-to-async wrapper
        In production, you might want to use actual async streaming
        """
        try:
            # The chatbot chain uses synchronous streaming
            # We wrap it to be compatible with async context
            for chunk in chain.stream({"input": user_message}, config=config):
                # Handle different chunk types from LangChain
                if isinstance(chunk, str):
                    yield chunk
                elif hasattr(chunk, "content"):
                    yield chunk.content
                else:
                    # Handle AIMessage or other types
                    yield str(chunk)
                    
        except Exception as e:
            raise AIServiceException(f"Streaming error: {str(e)}")
    
    def generate_conversation_title(self, first_message: str) -> str:
        """
        Generate a meaningful title from the first message
        
        Args:
            first_message: The first user message in the conversation
            
        Returns:
            Generated conversation title (max 50 chars)
        """
        # Simple title generation: take first 50 chars or first sentence
        title = first_message.strip()
        
        # Find first sentence ending
        for delimiter in ['.', '?', '!', '\n']:
            if delimiter in title:
                title = title.split(delimiter)[0]
                break
        
        # Truncate to 50 characters
        if len(title) > 50:
            title = title[:47] + "..."
        
        return title if title else "Nouvelle conversation"


class AIServiceException(Exception):
    """Custom exception for AI service errors"""
    pass


# Singleton instance
_ai_service_instance = None


def get_ai_service() -> AIService:
    """
    Dependency injection function for AIService
    Returns a singleton instance
    """
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance
