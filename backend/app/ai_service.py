import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from emergentintegrations.llm.chat import LlmChat, UserMessage
from .database import (
    chat_history_collection, 
    user_behavior_collection, 
    user_progress_collection,
    users_collection
)
from .models import User, UserBehavior
from dotenv import load_dotenv

load_dotenv()

class WellnessAIService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")
        self.system_message = """You are Welly, an AI wellness coach for Team Welly, a comprehensive health and wellness platform.

Your role:
- Provide personalized wellness recommendations based on user data
- Analyze user behavior patterns and progress
- Offer motivational support and encouragement
- Answer questions about health, fitness, nutrition, and mental wellness
- Guide users through wellness programs and challenges
- Provide insights on stress management, movement, and lifestyle

Guidelines:
- Be supportive, encouraging, and professional
- Use evidence-based wellness advice
- Personalize responses based on user's progress and goals
- Keep responses concise but helpful
- Encourage consistency and gradual improvement
- Reference specific programs and challenges when relevant
- Use a friendly, coaching tone

When analyzing user behavior, consider:
- Engagement patterns (frequency, duration)
- Preferred program types
- Challenge completion rates
- Progress trends
- Time of day preferences
- Consistency patterns

Always prioritize user safety and suggest consulting healthcare professionals for serious health concerns."""

    async def get_chat_response(self, user_id: str, message: str, session_id: str) -> Dict[str, Any]:
        """Get AI response to user message with behavior analysis"""
        try:
            # Get user data for personalization
            user_data = await self._get_user_context(user_id)
            
            # Create personalized system message
            personalized_system = self._create_personalized_system_message(user_data)
            
            # Initialize chat with Gemini
            chat = LlmChat(
                api_key=self.gemini_api_key,
                session_id=session_id,
                system_message=personalized_system
            ).with_model("gemini", "gemini-2.0-flash")
            
            # Get recent chat history for context
            recent_messages = await self._get_recent_chat_history(user_id, session_id)
            
            # Create user message with context
            contextual_message = self._create_contextual_message(message, user_data, recent_messages)
            user_message = UserMessage(text=contextual_message)
            
            # Get AI response
            ai_response = await chat.send_message(user_message)
            
            # Save chat history
            await self._save_chat_message(user_id, session_id, message, ai_response, user_data)
            
            # Generate user insights
            insights = await self._generate_user_insights(user_id, user_data)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(user_id, user_data)
            
            return {
                "response": ai_response,
                "insights": insights,
                "recommendations": recommendations,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            print(f"Error in AI service: {e}")
            return {
                "response": "I'm sorry, I'm having trouble processing your request right now. Please try again in a moment.",
                "insights": None,
                "recommendations": [],
                "timestamp": datetime.utcnow()
            }

    async def _get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user context for personalization"""
        user_doc = await users_collection.find_one({"_id": user_id})
        progress_doc = await user_progress_collection.find_one({"user_id": user_id})
        
        # Get recent behavior (last 7 days)
        recent_behavior_query = user_behavior_collection.find(
            {
                "user_id": user_id,
                "timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}
            }
        ).sort("timestamp", -1).limit(50)
        recent_behavior = await recent_behavior_query.to_list(length=50)
        
        return {
            "user": user_doc,
            "progress": progress_doc,
            "recent_behavior": recent_behavior,
            "goals": user_doc.get("selected_goals", []) if user_doc else [],
            "assessment": user_doc.get("assessment_data", {}) if user_doc else {}
        }

    def _create_personalized_system_message(self, user_data: Dict[str, Any]) -> str:
        """Create personalized system message based on user data"""
        base_message = self.system_message
        
        user = user_data.get("user", {})
        progress = user_data.get("progress", {})
        goals = user_data.get("goals", [])
        assessment = user_data.get("assessment", {})
        
        personalization = f"""

User Profile:
- Name: {user.get('name', 'User')}
- Plan: {user.get('plan', 'basic')}
- Goals: {', '.join(goals) if goals else 'General wellness'}
- Current streak: {progress.get('current_streak', 0) if progress else 0} days
- WellyPoints: {progress.get('welly_points', 0) if progress else 0}

Assessment Data:
- Stress level: {assessment.get('stressLevel', 'Unknown')}
- Sleep quality: {assessment.get('sleepQuality', 'Unknown')}
- Pain areas: {', '.join(assessment.get('painAreas', [])) if assessment.get('painAreas') else 'None specified'}
- Movement habits: {assessment.get('movementHabits', 'Unknown')}

Tailor your responses to this user's specific situation and goals."""
        
        return base_message + personalization

    async def _get_recent_chat_history(self, user_id: str, session_id: str) -> List[Dict[str, Any]]:
        """Get recent chat history for context"""
        chat_query = chat_history_collection.find(
            {
                "user_id": user_id,
                "session_id": session_id
            }
        ).sort("timestamp", -1).limit(5)
        return await chat_query.to_list(length=5)

    def _create_contextual_message(self, message: str, user_data: Dict[str, Any], recent_messages: List[Dict[str, Any]]) -> str:
        """Create contextual message with user data"""
        context = f"User message: {message}\n\n"
        
        # Add recent behavior insights
        recent_behavior = user_data.get("recent_behavior", [])
        if recent_behavior:
            behavior_summary = self._analyze_recent_behavior(recent_behavior)
            context += f"Recent activity context: {behavior_summary}\n\n"
        
        # Add recent chat context
        if recent_messages:
            context += "Recent conversation context:\n"
            for msg in reversed(recent_messages[-3:]):  # Last 3 messages
                context += f"- {msg.get('user_message', '')}\n"
            context += "\n"
        
        return context

    def _analyze_recent_behavior(self, behavior_data: List[Dict[str, Any]]) -> str:
        """Analyze recent user behavior for insights"""
        if not behavior_data:
            return "No recent activity"
        
        # Analyze patterns
        actions = [b.get("action", "") for b in behavior_data]
        pages = [b.get("page", "") for b in behavior_data]
        
        # Count activities
        action_counts = {}
        page_counts = {}
        
        for action in actions:
            action_counts[action] = action_counts.get(action, 0) + 1
        
        for page in pages:
            page_counts[page] = page_counts.get(page, 0) + 1
        
        # Generate summary
        summary = f"User has been active with {len(behavior_data)} actions in the last 7 days. "
        
        if action_counts:
            top_action = max(action_counts, key=action_counts.get)
            summary += f"Most frequent activity: {top_action} ({action_counts[top_action]} times). "
        
        if page_counts:
            top_page = max(page_counts, key=page_counts.get)
            summary += f"Most visited section: {top_page}. "
        
        return summary

    async def _save_chat_message(self, user_id: str, session_id: str, user_message: str, ai_response: str, user_data: Dict[str, Any]):
        """Save chat message to database"""
        chat_doc = {
            "user_id": user_id,
            "session_id": session_id,
            "user_message": user_message,
            "ai_response": ai_response,
            "timestamp": datetime.utcnow(),
            "user_context": {
                "goals": user_data.get("goals", []),
                "current_streak": user_data.get("progress", {}).get("current_streak", 0),
                "welly_points": user_data.get("progress", {}).get("welly_points", 0)
            }
        }
        
        await chat_history_collection.insert_one(chat_doc)

    async def _generate_user_insights(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights about user behavior and progress"""
        progress = user_data.get("progress", {})
        recent_behavior = user_data.get("recent_behavior", [])
        
        insights = {
            "engagement_level": self._calculate_engagement_level(recent_behavior),
            "consistency_score": progress.get("current_streak", 0) * 10,
            "preferred_activities": self._get_preferred_activities(recent_behavior),
            "progress_trend": self._calculate_progress_trend(user_id, progress),
            "time_of_day_preference": self._get_time_preferences(recent_behavior)
        }
        
        return insights

    def _calculate_engagement_level(self, recent_behavior: List[Dict[str, Any]]) -> str:
        """Calculate user engagement level"""
        if not recent_behavior:
            return "low"
        
        activity_count = len(recent_behavior)
        unique_days = len(set(b.get("timestamp", datetime.utcnow()).date() for b in recent_behavior))
        
        if activity_count >= 20 and unique_days >= 5:
            return "high"
        elif activity_count >= 10 and unique_days >= 3:
            return "medium"
        else:
            return "low"

    def _get_preferred_activities(self, recent_behavior: List[Dict[str, Any]]) -> List[str]:
        """Get user's preferred activities"""
        activity_counts = {}
        
        for behavior in recent_behavior:
            page = behavior.get("page", "")
            if page:
                activity_counts[page] = activity_counts.get(page, 0) + 1
        
        # Return top 3 activities
        return sorted(activity_counts.keys(), key=lambda x: activity_counts[x], reverse=True)[:3]

    def _calculate_progress_trend(self, user_id: str, progress: Dict[str, Any]) -> str:
        """Calculate progress trend"""
        current_streak = progress.get("current_streak", 0)
        welly_points = progress.get("welly_points", 0)
        
        if current_streak >= 7 and welly_points >= 500:
            return "excellent"
        elif current_streak >= 3 and welly_points >= 200:
            return "good"
        elif current_streak >= 1 and welly_points >= 50:
            return "improving"
        else:
            return "needs_motivation"

    def _get_time_preferences(self, recent_behavior: List[Dict[str, Any]]) -> str:
        """Get user's time of day preferences"""
        if not recent_behavior:
            return "unknown"
        
        hour_counts = {}
        for behavior in recent_behavior:
            timestamp = behavior.get("timestamp", datetime.utcnow())
            hour = timestamp.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        if not hour_counts:
            return "unknown"
        
        peak_hour = max(hour_counts, key=hour_counts.get)
        
        if 6 <= peak_hour <= 11:
            return "morning"
        elif 12 <= peak_hour <= 17:
            return "afternoon"
        else:
            return "evening"

    async def _generate_recommendations(self, user_id: str, user_data: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        progress = user_data.get("progress", {})
        goals = user_data.get("goals", [])
        recent_behavior = user_data.get("recent_behavior", [])
        
        # Streak-based recommendations
        current_streak = progress.get("current_streak", 0)
        if current_streak == 0:
            recommendations.append("Start with a simple 5-minute morning stretch to build your wellness habit")
        elif current_streak < 3:
            recommendations.append("You're building momentum! Try adding a breathing exercise to your routine")
        elif current_streak >= 7:
            recommendations.append("Amazing streak! Consider exploring new program categories to keep things fresh")
        
        # Goal-based recommendations
        if "Reduce Pain" in goals:
            recommendations.append("Check out our Pain to Performance programs for targeted relief")
        if "Improve Flexibility" in goals:
            recommendations.append("Daily stretching can significantly improve flexibility - try our Mobility programs")
        if "Boost Mental Health" in goals:
            recommendations.append("Mindfulness and breathing exercises can greatly improve mental wellness")
        
        # Activity-based recommendations
        engagement_level = self._calculate_engagement_level(recent_behavior)
        if engagement_level == "low":
            recommendations.append("Try setting a daily reminder to complete one quick wellness activity")
        elif engagement_level == "high":
            recommendations.append("Consider booking a 1-on-1 coaching session to take your wellness to the next level")
        
        return recommendations[:5]  # Return max 5 recommendations

# Initialize the AI service
ai_service = WellnessAIService()