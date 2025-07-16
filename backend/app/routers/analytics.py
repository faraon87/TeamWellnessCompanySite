from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from datetime import datetime, timedelta
from ..models import User
from ..auth import get_current_user
from ..behavior_tracker import BehaviorTracker
from ..database import user_behavior_collection, user_progress_collection

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/user")
async def get_user_analytics(current_user: User = Depends(get_current_user)):
    """Get comprehensive user analytics"""
    try:
        analytics = await BehaviorTracker.get_user_analytics(current_user.id)
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user analytics: {str(e)}")

@router.get("/behavior")
async def get_behavior_analytics(
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """Get behavior analytics for specified time period"""
    try:
        # Get behavior data
        start_date = datetime.utcnow() - timedelta(days=days)
        
        behaviors = user_behavior_collection.find(
            {
                "user_id": current_user.id,
                "timestamp": {"$gte": start_date}
            }
        ).sort("timestamp", -1)
        behaviors = await behaviors.to_list(length=1000)
        
        # Analyze behavior patterns
        analytics = {
            "period_days": days,
            "total_actions": len(behaviors),
            "daily_average": len(behaviors) / days if days > 0 else 0,
            "action_breakdown": _analyze_actions(behaviors),
            "page_usage": _analyze_page_usage(behaviors),
            "hourly_activity": _analyze_hourly_activity(behaviors),
            "daily_activity": _analyze_daily_activity(behaviors),
            "engagement_trend": _analyze_engagement_trend(behaviors, days)
        }
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get behavior analytics: {str(e)}")

@router.get("/progress")
async def get_progress_analytics(current_user: User = Depends(get_current_user)):
    """Get progress analytics"""
    try:
        # Get user progress
        progress = await user_progress_collection.find_one({"user_id": current_user.id})
        
        if not progress:
            return {"message": "No progress data found"}
        
        # Calculate analytics
        analytics = {
            "current_metrics": {
                "welly_points": progress.get("welly_points", 0),
                "current_streak": progress.get("current_streak", 0),
                "completed_programs": len(progress.get("completed_programs", [])),
                "completed_challenges": len(progress.get("completed_challenges", [])),
                "bookmarked_programs": len(progress.get("bookmarked_programs", []))
            },
            "completion_rates": {
                "daily": progress.get("daily_completion", 0),
                "weekly": progress.get("weekly_completion", 0),
                "monthly": progress.get("monthly_completion", 0)
            },
            "last_activity": progress.get("last_activity"),
            "progress_trend": _calculate_progress_trend(progress)
        }
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get progress analytics: {str(e)}")

@router.get("/wellness-score")
async def get_wellness_score(current_user: User = Depends(get_current_user)):
    """Calculate and return user's wellness score"""
    try:
        # Get user data
        progress = await user_progress_collection.find_one({"user_id": current_user.id})
        
        # Get recent behavior (last 7 days)
        recent_behaviors = await user_behavior_collection.find(
            {
                "user_id": current_user.id,
                "timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}
            }
        ).to_list(length=100)
        
        # Calculate wellness score components
        score_components = {
            "consistency": _calculate_consistency_score(progress),
            "engagement": _calculate_engagement_score(recent_behaviors),
            "progress": _calculate_progress_score(progress),
            "variety": _calculate_variety_score(recent_behaviors)
        }
        
        # Calculate overall wellness score (0-100)
        overall_score = sum(score_components.values()) / len(score_components)
        
        return {
            "overall_score": round(overall_score, 1),
            "score_components": score_components,
            "score_breakdown": _get_score_breakdown(score_components),
            "recommendations": _get_score_recommendations(score_components)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get wellness score: {str(e)}")

def _analyze_actions(behaviors: List[Dict[str, Any]]) -> Dict[str, int]:
    """Analyze action breakdown"""
    action_counts = {}
    for behavior in behaviors:
        action = behavior.get("action", "unknown")
        action_counts[action] = action_counts.get(action, 0) + 1
    return action_counts

def _analyze_page_usage(behaviors: List[Dict[str, Any]]) -> Dict[str, int]:
    """Analyze page usage"""
    page_counts = {}
    for behavior in behaviors:
        page = behavior.get("page", "unknown")
        page_counts[page] = page_counts.get(page, 0) + 1
    return page_counts

def _analyze_hourly_activity(behaviors: List[Dict[str, Any]]) -> Dict[int, int]:
    """Analyze activity by hour"""
    hourly_counts = {}
    for behavior in behaviors:
        hour = behavior.get("timestamp", datetime.utcnow()).hour
        hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
    return hourly_counts

def _analyze_daily_activity(behaviors: List[Dict[str, Any]]) -> Dict[str, int]:
    """Analyze activity by day of week"""
    daily_counts = {}
    for behavior in behaviors:
        day = behavior.get("timestamp", datetime.utcnow()).strftime("%A")
        daily_counts[day] = daily_counts.get(day, 0) + 1
    return daily_counts

def _analyze_engagement_trend(behaviors: List[Dict[str, Any]], days: int) -> Dict[str, Any]:
    """Analyze engagement trend"""
    if not behaviors:
        return {"trend": "stable", "change_percentage": 0}
    
    # Split into first and second half
    mid_point = len(behaviors) // 2
    first_half = behaviors[:mid_point]
    second_half = behaviors[mid_point:]
    
    first_half_avg = len(first_half) / (days / 2) if days > 0 else 0
    second_half_avg = len(second_half) / (days / 2) if days > 0 else 0
    
    if first_half_avg == 0:
        change_percentage = 0
        trend = "stable"
    else:
        change_percentage = ((second_half_avg - first_half_avg) / first_half_avg) * 100
        if change_percentage > 10:
            trend = "increasing"
        elif change_percentage < -10:
            trend = "decreasing"
        else:
            trend = "stable"
    
    return {
        "trend": trend,
        "change_percentage": round(change_percentage, 1),
        "first_period_avg": round(first_half_avg, 1),
        "second_period_avg": round(second_half_avg, 1)
    }

def _calculate_progress_trend(progress: Dict[str, Any]) -> str:
    """Calculate progress trend"""
    welly_points = progress.get("welly_points", 0)
    current_streak = progress.get("current_streak", 0)
    completed_programs = len(progress.get("completed_programs", []))
    
    if welly_points > 1000 and current_streak > 7:
        return "excellent"
    elif welly_points > 500 and current_streak > 3:
        return "good"
    elif welly_points > 100 and current_streak > 1:
        return "improving"
    else:
        return "starting"

def _calculate_consistency_score(progress: Dict[str, Any]) -> float:
    """Calculate consistency score (0-100)"""
    if not progress:
        return 0.0
    
    current_streak = progress.get("current_streak", 0)
    
    # Score based on streak length
    if current_streak >= 30:
        return 100.0
    elif current_streak >= 14:
        return 80.0
    elif current_streak >= 7:
        return 60.0
    elif current_streak >= 3:
        return 40.0
    elif current_streak >= 1:
        return 20.0
    else:
        return 0.0

def _calculate_engagement_score(behaviors: List[Dict[str, Any]]) -> float:
    """Calculate engagement score (0-100)"""
    if not behaviors:
        return 0.0
    
    # Score based on activity volume in last 7 days
    action_count = len(behaviors)
    unique_days = len(set(b.get("timestamp", datetime.utcnow()).date() for b in behaviors))
    
    # Base score on actions per day
    daily_average = action_count / 7
    
    if daily_average >= 10:
        return 100.0
    elif daily_average >= 5:
        return 80.0
    elif daily_average >= 3:
        return 60.0
    elif daily_average >= 1:
        return 40.0
    else:
        return 20.0

def _calculate_progress_score(progress: Dict[str, Any]) -> float:
    """Calculate progress score (0-100)"""
    if not progress:
        return 0.0
    
    welly_points = progress.get("welly_points", 0)
    completed_programs = len(progress.get("completed_programs", []))
    
    # Score based on points and completion
    points_score = min(50, welly_points / 20)  # 50 points max from WellyPoints
    completion_score = min(50, completed_programs * 5)  # 50 points max from completions
    
    return points_score + completion_score

def _calculate_variety_score(behaviors: List[Dict[str, Any]]) -> float:
    """Calculate activity variety score (0-100)"""
    if not behaviors:
        return 0.0
    
    unique_actions = len(set(b.get("action", "") for b in behaviors))
    unique_pages = len(set(b.get("page", "") for b in behaviors))
    
    # Score based on variety of activities
    variety_score = min(100, (unique_actions * 10) + (unique_pages * 5))
    
    return variety_score

def _get_score_breakdown(score_components: Dict[str, float]) -> Dict[str, str]:
    """Get score breakdown descriptions"""
    breakdown = {}
    
    for component, score in score_components.items():
        if score >= 80:
            breakdown[component] = "Excellent"
        elif score >= 60:
            breakdown[component] = "Good"
        elif score >= 40:
            breakdown[component] = "Fair"
        else:
            breakdown[component] = "Needs Improvement"
    
    return breakdown

def _get_score_recommendations(score_components: Dict[str, float]) -> List[str]:
    """Get recommendations based on score components"""
    recommendations = []
    
    if score_components.get("consistency", 0) < 60:
        recommendations.append("Try to log in daily to build consistency")
    
    if score_components.get("engagement", 0) < 60:
        recommendations.append("Increase your daily activity to improve engagement")
    
    if score_components.get("progress", 0) < 60:
        recommendations.append("Complete more programs and challenges for better progress")
    
    if score_components.get("variety", 0) < 60:
        recommendations.append("Explore different sections of the app for more variety")
    
    return recommendations