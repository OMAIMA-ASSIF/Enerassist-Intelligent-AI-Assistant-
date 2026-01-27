"""
Chat Routes - Main chatbot API endpoints
Handles AI conversation interactions
"""
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from server.middlewares.auth import get_current_user
from server.models import ChatRequest, ChatResponse, MessageBase, MessageResponse
from server.services import (
    get_ai_service,
    get_conversation_service,
    get_history_service,
    AIService,
    ConversationService,
    HistoryService
)

router = APIRouter()


@router.post("/send", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_message(
    chat_request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    ai_service: AIService = Depends(get_ai_service),
    conversation_service: ConversationService = Depends(get_conversation_service),
    history_service: HistoryService = Depends(get_history_service)
):
    """
    Send a message to the AI chatbot
    
    Flow:
    1. Validate or create conversation
    2. Fetch conversation context
    3. Call AI model with context
    4. Store user message + AI response
    5. Return response
    
    Authentication: Required (JWT)
    """
    try:
        user_id = str(current_user["_id"])
        
        # Step 1: Get or create user's history
        historique_id = await history_service.get_or_create_history(user_id)
        
        # Step 2: Determine conversation ID
        is_new_conversation = False
        conversation_id = chat_request.conversation_id
        
        if not conversation_id:
            # Create new conversation
            is_new_conversation = True
            
            # Generate title from first message if not provided
            titre = chat_request.conversation_title
            if not titre:
                titre = ai_service.generate_conversation_title(chat_request.message)
            
            conversation_id = await conversation_service.create_conversation(
                historique_id=historique_id,
                titre=titre,
                initial_messages=[]
            )
        else:
            # Validate that conversation belongs to user
            try:
                await conversation_service.get_conversation_by_id(
                    conversation_id=conversation_id,
                    historique_id=historique_id
                )
            except HTTPException as e:
                if e.status_code == status.HTTP_404_NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You don't have access to this conversation"
                    )
                raise
        
        # Step 3: Fetch conversation for context
        conversation = await conversation_service.get_conversation_by_id(
            conversation_id=conversation_id,
            historique_id=historique_id
        )
        
        # Step 4: Call AI model
        try:
            ai_response_text = await ai_service.generate_response(
                user_message=chat_request.message,
                conversation_id=conversation_id,
                chat_history=conversation.messages
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI model error: {str(e)}"
            )
        
        # Step 5: Create message objects
        user_message = MessageBase(
            role="user",
            texte=chat_request.message,
            date=datetime.utcnow()
        )
        
        assistant_message = MessageBase(
            role="assistant",
            texte=ai_response_text,
            date=datetime.utcnow()
        )
        
        # Step 6: Store messages in conversation
        await conversation_service.add_messages(
            conversation_id=conversation_id,
            historique_id=historique_id,
            messages=[user_message, assistant_message]
        )
        
        # Step 7: Return response
        return ChatResponse(
            conversation_id=conversation_id,
            user_message=MessageResponse(**user_message.model_dump()),
            assistant_message=MessageResponse(**assistant_message.model_dump()),
            is_new_conversation=is_new_conversation
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def chat_health_check():
    """
    Health check endpoint for chat service
    No authentication required
    """
    return {
        "status": "healthy",
        "service": "chat",
        "timestamp": datetime.utcnow().isoformat()
    }
