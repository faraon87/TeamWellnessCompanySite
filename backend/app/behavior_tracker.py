from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from .database import user_behavior_collection, user_progress_collection
from .models import UserBehavior

class BehaviorTracker:
    """Track and analyze user behavior for wellness insights"""
    
    @staticmethod
    async def track_action(
        user_id: str, 
        action: str, 
        page: str, 
        details: Dict[str, Any] = None,
        session_id: Optional[str] = None
    ):
        """Track a user action"""
        behavior = UserBehavior(
            user_id=user_id,
            action=action,
            page=page,
            details=details or {},
            session_id=session_id,
            timestamp=datetime.utcnow()
        )
        
        await user_behavior_collection.insert_one(behavior.dict())
        
        # Update user progress based on action
        await BehaviorTracker._update_progress(user_id, action, details or {})
    
    @staticmethod
    async def _update_progress(user_id: str, action: str, details: Dict[str, Any]):
        """Update user progress based on action"""
        progress_update = {}
        
        # Award points for different actions
        points_awarded = 0
        
        if action == "complete_program":
            points_awarded = 50
            await BehaviorTracker._add_completed_program(user_id, details.get("program_id"))
        elif action == "start_program":
            points_awarded = 10
        elif action == "complete_challenge":
            points_awarded = details.get("challenge_points", 30)
            await BehaviorTracker._add_completed_challenge(user_id, details.get("challenge_id"))
        elif action == "chat_interaction":
            points_awarded = 5
        elif action == "login":
            points_awarded = 5
            await BehaviorTracker._update_streak(user_id)
        elif action == "book_session":
            points_awarded = 20
        elif action == "bookmark_program":
            points_awarded = 5
        
        if points_awarded > 0:
            await user_progress_collection.update_one(
                {"user_id": user_id},
                {
                    "$inc": {"welly_points": points_awarded},
                    "$set": {"last_activity": datetime.utcnow(), "updated_at": datetime.utcnow()}
                },
                upsert=True
            )
    
    @staticmethod
    async def _add_completed_program(user_id: str, program_id: str):
        """Add a completed program to user's progress"""
        if program_id:
            await user_progress_collection.update_one(
                {"user_id": user_id},
                {"$addToSet": {"completed_programs": program_id}},
                upsert=True
            )
    
    @staticmethod
    async def _add_completed_challenge(user_id: str, challenge_id: str):
        """Add a completed challenge to user's progress"""
        if challenge_id:
            await user_progress_collection.update_one(
                {"user_id": user_id},
                {"$addToSet": {"completed_challenges": challenge_id}},
                upsert=True
            )
    
    @staticmethod
    async def _update_streak(user_id: str):
        """Update user's daily streak"""
        today = datetime.utcnow().date()
        
        progress = await user_progress_collection.find_one({"user_id": user_id})
        
        if progress:
            last_activity = progress.get("last_activity")
            if last_activity:
                last_activity_date = last_activity.date()
                
                if last_activity_date == today:
                    # Already logged today, no streak update needed
                    return
                elif last_activity_date == today - timedelta(days=1):
                    # Consecutive day, increment streak
                    await user_progress_collection.update_one(
                        {"user_id": user_id},
                        {"$inc": {"current_streak": 1}}
                    )
                else:
                    # Streak broken, reset to 1
                    await user_progress_collection.update_one(
                        {"user_id": user_id},
                        {"$set": {"current_streak": 1}}
                    )
            else:
                # First time logging, start streak
                await user_progress_collection.update_one(
                    {"user_id": user_id},
                    {"$set": {"current_streak": 1}}
                )
    
    @staticmethod
    async def get_user_analytics(user_id: str) -> Dict[str, Any]:
        """Get comprehensive user analytics"""
        # Get user behavior from last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        behaviors = user_behavior_collection.find(
            {
                "user_id": user_id,
                "timestamp": {"$gte": thirty_days_ago}
            }
        ).sort("timestamp", -1)
        behaviors = await behaviors.to_list(length=1000)
        
        # Get user progress
        progress = await user_progress_collection.find_one({"user_id": user_id})
        
        # Analyze behavior patterns
        analytics = {
            "total_actions": len(behaviors),
            "unique_days_active": len(set(b["timestamp"].date() for b in behaviors)),
            "most_active_page": BehaviorTracker._get_most_active_page(behaviors),
            "activity_by_hour": BehaviorTracker._get_activity_by_hour(behaviors),
            "weekly_activity": BehaviorTracker._get_weekly_activity(behaviors),
            "engagement_score": BehaviorTracker._calculate_engagement_score(behaviors),
            "progress_data": progress or {},
            "recommendations": BehaviorTracker._generate_behavior_recommendations(behaviors, progress)
        }
        
        return analytics
    
    @staticmethod
    def _get_most_active_page(behaviors: list) -> str:
        """Get the most visited page"""
        if not behaviors:
            return "dashboard"
        
        page_counts = {}
        for behavior in behaviors:
            page = behavior.get("page", "")
            page_counts[page] = page_counts.get(page, 0) + 1
        
        return max(page_counts, key=page_counts.get) if page_counts else "dashboard"
    
    @staticmethod
    def _get_activity_by_hour(behaviors: list) -> Dict[int, int]:
        """Get activity distribution by hour of day"""
        hour_counts = {}
        for behavior in behaviors:
            hour = behavior["timestamp"].hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        return hour_counts
    
    @staticmethod
    def _get_weekly_activity(behaviors: list) -> Dict[str, int]:
        """Get activity distribution by day of week"""
        day_counts = {}
        for behavior in behaviors:
            day = behavior["timestamp"].strftime("%A")
            day_counts[day] = day_counts.get(day, 0) + 1
        
        return day_counts
    
    @staticmethod
    def _calculate_engagement_score(behaviors: list) -> float:
        """Calculate user engagement score (0-100)"""
        if not behaviors:
            return 0.0
        
        # Factors for engagement score
        total_actions = len(behaviors)
        unique_days = len(set(b["timestamp"].date() for b in behaviors))
        action_variety = len(set(b["action"] for b in behaviors))
        
        # Calculate score
        score = min(100, (total_actions * 2) + (unique_days * 5) + (action_variety * 3))
        
        return round(score, 1)
    
    @staticmethod
    def _generate_behavior_recommendations(behaviors: list, progress: dict) -> list:
        """Generate recommendations based on behavior patterns"""
        recommendations = []
        
        if not behaviors:
            recommendations.append("Start exploring the app - try completing your first program!")
            return recommendations
        
        # Analyze patterns
        action_counts = {}
        for behavior in behaviors:
            action = behavior.get("action", "")
            action_counts[action] = action_counts.get(action, 0) + 1
        
        # Generate recommendations
        if action_counts.get("complete_program", 0) < 3:
            recommendations.append("Try completing more programs to build your wellness routine")
        
        if action_counts.get("chat_interaction", 0) < 5:
            recommendations.append("Chat with Welly AI for personalized wellness guidance")
        
        if action_counts.get("book_session", 0) == 0:
            recommendations.append("Consider booking a coaching session for personalized support")
        
        if progress and progress.get("current_streak", 0) < 3:
            recommendations.append("Build consistency by logging in daily for better results")
        
        return recommendations[:3]  # Return max 3 recommendations