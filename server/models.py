"""
MongoDB Data Models and Pydantic Schemas
Handles all data structures for the chatbot application
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

# ==================== Helper Classes ====================

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic v2 compatibility"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


# ==================== Message Models ====================

class MessageBase(BaseModel):
    """Base message structure"""
    role: str = Field(..., pattern="^(user|assistant)$", description="Message role: user or assistant")
    texte: str = Field(..., min_length=1, max_length=10000, description="Message content")
    date: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MessageResponse(MessageBase):
    """Message response model for API responses"""
    pass


# ==================== Conversation Models ====================

class ConversationBase(BaseModel):
    """Base conversation structure"""
    titre: str = Field(default="Nouvelle conversation", max_length=200, description="Conversation title")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation"""
    pass


class ConversationInDB(ConversationBase):
    """Conversation as stored in MongoDB"""
    id: str = Field(alias="_id")
    historique_id: str
    messages: List[MessageBase] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class ConversationResponse(BaseModel):
    """Conversation response for API"""
    id: str
    titre: str
    messages: List[MessageResponse]
    created_at: str
    last_updated: str
    message_count: int


class ConversationListItem(BaseModel):
    """Lightweight conversation item for listing"""
    id: str
    titre: str
    last_updated: str
    message_count: int
    preview: Optional[str] = None  # First user message preview


# ==================== History Models ====================

class HistoryBase(BaseModel):
    """Base history structure"""
    user_id: str


class HistoryInDB(HistoryBase):
    """History as stored in MongoDB"""
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class HistoryResponse(BaseModel):
    """History response with all conversations"""
    id: str
    user_id: str
    conversations: List[ConversationListItem]
    total_conversations: int
    created_at: str
    updated_at: str


# ==================== Chat Request/Response Models ====================

class ChatRequest(BaseModel):
    """Request model for sending a message"""
    conversation_id: Optional[str] = Field(None, description="Conversation ID (if continuing), None for new conversation")
    message: str = Field(..., min_length=1, max_length=10000, description="User's message")
    conversation_title: Optional[str] = Field(None, max_length=200, description="Title for new conversation")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    conversation_id: str
    user_message: MessageResponse
    assistant_message: MessageResponse
    is_new_conversation: bool = False


# ==================== Pagination Models ====================

class PaginationParams(BaseModel):
    """Pagination parameters"""
    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum number of items to return")


class ConversationListResponse(BaseModel):
    """Paginated conversation list response"""
    conversations: List[ConversationListItem]
    total: int
    skip: int
    limit: int
    has_more: bool
