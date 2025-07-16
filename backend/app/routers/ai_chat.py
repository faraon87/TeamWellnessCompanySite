from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from datetime import datetime
import uuid
from ..models import User, ChatMessage, ChatResponse
from ..auth import get_current_user
from ..ai_service import ai_service
from ..behavior_tracker import BehaviorTracker

router = APIRouter(prefix="/api/ai", tags=["ai_chat"])

@router.post("/chat")
async def chat_with_ai(
    message: ChatMessage,
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """Chat with Welly AI assistant"""
    try:
        # Generate session ID if not provided
        if not message.session_id:
            message.session_id = str(uuid.uuid4())
        
        # Get AI response with behavior analysis
        ai_response = await ai_service.get_chat_response(
            user_id=current_user.id,
            message=message.message,
            session_id=message.session_id
        )
        
        # Track chat interaction
        await BehaviorTracker.track_action(
            user_id=current_user.id,
            action="chat_interaction",
            page="ai_chat",
            details={
                "message_length": len(message.message),
                "session_id": message.session_id,
                "response_generated": True
            },
            session_id=message.session_id
        )
        
        return ChatResponse(
            response=ai_response["response"],
            timestamp=ai_response["timestamp"],
            user_insights=ai_response.get("insights"),
            recommendations=ai_response.get("recommendations", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI chat failed: {str(e)}")

@router.get("/insights")
async def get_user_insights(current_user: User = Depends(get_current_user)):
    """Get AI-generated user insights"""
    try:
        # Get user context for insights
        user_context = await ai_service._get_user_context(current_user.id)
        
        # Generate insights
        insights = await ai_service._generate_user_insights(current_user.id, user_context)
        
        # Generate recommendations
        recommendations = await ai_service._generate_recommendations(current_user.id, user_context)
        
        return {
            "user_insights": insights,
            "recommendations": recommendations,
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get insights: {str(e)}")

@router.get("/chat/history")
async def get_chat_history(
    session_id: str = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """Get chat history for user"""
    try:
        from ..database import chat_history_collection
        
        # Build query
        query = {"user_id": current_user.id}
        if session_id:
            query["session_id"] = session_id
        
        # Get chat history
        chat_query = chat_history_collection.find(query).sort("timestamp", -1).limit(limit)
        chat_history = await chat_query.to_list(length=limit)
        
        return {"chat_history": chat_history}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get chat history: {str(e)}")

@router.post("/feedback")
async def provide_feedback(
    feedback_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Provide feedback on AI responses"""
    try:
        # Track feedback
        await BehaviorTracker.track_action(
            user_id=current_user.id,
            action="ai_feedback",
            page="ai_chat",
            details=feedback_data
        )
        
        return {"message": "Feedback recorded successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record feedback: {str(e)}")

@router.get("/wellness-tips")
async def get_wellness_tips(current_user: User = Depends(get_current_user)):
    """Get personalized wellness tips"""
    try:
        # Get user context
        user_context = await ai_service._get_user_context(current_user.id)
        
        # Generate personalized tips using AI
        tips_prompt = f"""Based on the user's wellness goals and current progress, provide 5 personalized wellness tips. 
        Goals: {', '.join(user_context.get('goals', []))}
        Current streak: {user_context.get('progress', {}).get('current_streak', 0)} days
        
        Make the tips specific, actionable, and encouraging."""
        
        # Create a temporary session for tips
        session_id = f"tips-{uuid.uuid4()}"
        
        tips_response = await ai_service.get_chat_response(
            user_id=current_user.id,
            message=tips_prompt,
            session_id=session_id
        )
        
        return {
            "wellness_tips": tips_response["response"],
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get wellness tips: {str(e)}")

@router.get("/motivation")
async def get_motivation(current_user: User = Depends(get_current_user)):
    """Get motivational message based on user progress"""
    try:
        # Get user context
        user_context = await ai_service._get_user_context(current_user.id)
        
        progress = user_context.get('progress', {})
        goals = user_context.get('goals', [])
        
        # Generate motivational message
        motivation_prompt = f"""Create a motivational message for a user with:
        - Current streak: {progress.get('current_streak', 0)} days
        - WellyPoints: {progress.get('welly_points', 0)}
        - Goals: {', '.join(goals)}
        
        Make it encouraging, personal, and inspiring. Keep it under 100 words."""
        
        session_id = f"motivation-{uuid.uuid4()}"
        
        motivation_response = await ai_service.get_chat_response(
            user_id=current_user.id,
            message=motivation_prompt,
            session_id=session_id
        )
        
        return {
            "motivation": motivation_response["response"],
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get motivation: {str(e)}")