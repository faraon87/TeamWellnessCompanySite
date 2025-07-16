from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from datetime import datetime
from ..models import User, Program
from ..database import programs_collection, user_progress_collection
from ..auth import get_current_user
from ..behavior_tracker import BehaviorTracker

router = APIRouter(prefix="/api/programs", tags=["programs"])

@router.get("/")
async def get_programs(
    category: str = None,
    level: str = None,
    current_user: User = Depends(get_current_user)
) -> List[Program]:
    """Get all programs with optional filtering"""
    try:
        # Build query
        query = {}
        if category:
            query["category"] = category
        if level:
            query["level"] = level
        
        # Get programs
        query_result = await programs_collection.find(query)
        programs = await query_result.sort("title", 1).to_list(length=100)
        
        # Track program browsing
        await BehaviorTracker.track_action(
            user_id=current_user.id,
            action="browse_programs",
            page="programs",
            details={
                "category": category,
                "level": level,
                "programs_count": len(programs)
            }
        )
        
        return programs
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get programs: {str(e)}")

@router.get("/{program_id}")
async def get_program(
    program_id: str,
    current_user: User = Depends(get_current_user)
) -> Program:
    """Get specific program details"""
    try:
        program = await programs_collection.find_one({"id": program_id})
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")
        
        # Track program view
        await BehaviorTracker.track_action(
            user_id=current_user.id,
            action="view_program",
            page="programs",
            details={
                "program_id": program_id,
                "program_title": program.get("title"),
                "category": program.get("category")
            }
        )
        
        return program
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get program: {str(e)}")

@router.post("/{program_id}/start")
async def start_program(
    program_id: str,
    current_user: User = Depends(get_current_user)
):
    """Start a program"""
    try:
        program = await programs_collection.find_one({"id": program_id})
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")
        
        # Track program start
        await BehaviorTracker.track_action(
            user_id=current_user.id,
            action="start_program",
            page="programs",
            details={
                "program_id": program_id,
                "program_title": program.get("title"),
                "category": program.get("category"),
                "duration": program.get("duration")
            }
        )
        
        return {"message": "Program started successfully", "program": program}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start program: {str(e)}")

@router.post("/{program_id}/complete")
async def complete_program(
    program_id: str,
    completion_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Mark program as completed"""
    try:
        program = await programs_collection.find_one({"id": program_id})
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")
        
        # Track program completion
        await BehaviorTracker.track_action(
            user_id=current_user.id,
            action="complete_program",
            page="programs",
            details={
                "program_id": program_id,
                "program_title": program.get("title"),
                "category": program.get("category"),
                "duration": program.get("duration"),
                "completion_rating": completion_data.get("rating"),
                "completion_notes": completion_data.get("notes")
            }
        )
        
        return {"message": "Program completed successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete program: {str(e)}")

@router.post("/{program_id}/bookmark")
async def bookmark_program(
    program_id: str,
    current_user: User = Depends(get_current_user)
):
    """Bookmark a program"""
    try:
        program = await programs_collection.find_one({"id": program_id})
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")
        
        # Add to bookmarks
        await user_progress_collection.update_one(
            {"user_id": current_user.id},
            {"$addToSet": {"bookmarked_programs": program_id}},
            upsert=True
        )
        
        # Track bookmark
        await BehaviorTracker.track_action(
            user_id=current_user.id,
            action="bookmark_program",
            page="programs",
            details={
                "program_id": program_id,
                "program_title": program.get("title"),
                "category": program.get("category")
            }
        )
        
        return {"message": "Program bookmarked successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to bookmark program: {str(e)}")

@router.delete("/{program_id}/bookmark")
async def remove_bookmark(
    program_id: str,
    current_user: User = Depends(get_current_user)
):
    """Remove bookmark from program"""
    try:
        # Remove from bookmarks
        await user_progress_collection.update_one(
            {"user_id": current_user.id},
            {"$pull": {"bookmarked_programs": program_id}}
        )
        
        # Track bookmark removal
        await BehaviorTracker.track_action(
            user_id=current_user.id,
            action="remove_bookmark",
            page="programs",
            details={"program_id": program_id}
        )
        
        return {"message": "Bookmark removed successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove bookmark: {str(e)}")

@router.get("/categories/stats")
async def get_category_stats(current_user: User = Depends(get_current_user)):
    """Get program statistics by category"""
    try:
        # Get all programs
        programs = await programs_collection.find().to_list(length=1000)
        
        # Get user progress
        user_progress = await user_progress_collection.find_one({"user_id": current_user.id})
        completed_programs = user_progress.get("completed_programs", []) if user_progress else []
        bookmarked_programs = user_progress.get("bookmarked_programs", []) if user_progress else []
        
        # Calculate stats by category
        category_stats = {}
        for program in programs:
            category = program.get("category", "general")
            if category not in category_stats:
                category_stats[category] = {
                    "total_programs": 0,
                    "completed": 0,
                    "bookmarked": 0,
                    "completion_rate": 0
                }
            
            category_stats[category]["total_programs"] += 1
            
            if program.get("id") in completed_programs:
                category_stats[category]["completed"] += 1
            
            if program.get("id") in bookmarked_programs:
                category_stats[category]["bookmarked"] += 1
        
        # Calculate completion rates
        for category in category_stats:
            if category_stats[category]["total_programs"] > 0:
                category_stats[category]["completion_rate"] = (
                    category_stats[category]["completed"] / 
                    category_stats[category]["total_programs"]
                ) * 100
        
        return {"category_stats": category_stats}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get category stats: {str(e)}")

@router.get("/recommendations")
async def get_program_recommendations(current_user: User = Depends(get_current_user)):
    """Get personalized program recommendations"""
    try:
        # Get user data
        user_doc = await user_progress_collection.find_one({"user_id": current_user.id})
        completed_programs = user_doc.get("completed_programs", []) if user_doc else []
        
        # Get user goals
        user_info = await user_progress_collection.find_one({"user_id": current_user.id})
        goals = user_info.get("selected_goals", []) if user_info else []
        
        # Get programs not yet completed
        all_programs = await programs_collection.find().to_list(length=1000)
        
        # Filter and recommend programs
        recommendations = []
        for program in all_programs:
            if program.get("id") not in completed_programs:
                # Simple recommendation logic based on goals
                if any(goal.lower() in program.get("description", "").lower() for goal in goals):
                    recommendations.append(program)
        
        # Limit to top 5 recommendations
        recommendations = recommendations[:5]
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")