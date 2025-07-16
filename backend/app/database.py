from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import uuid
from dotenv import load_dotenv

load_dotenv()

# In-memory database for development
_memory_db = {
    "users": {},
    "sessions": {},
    "programs": {},
    "user_progress": {},
    "chat_history": {},
    "payment_transactions": {},
    "user_behavior": {},
    "challenges": {},
    "bookings": {},
    "notifications": {},
    "wellness_packages": {}
}

class MemoryCollection:
    """In-memory collection that mimics MongoDB collection interface"""
    
    def __init__(self, name: str):
        self.name = name
        self.data = _memory_db[name]
    
    async def insert_one(self, document: Dict[str, Any]):
        """Insert a single document"""
        doc_id = str(uuid.uuid4())
        document["_id"] = doc_id
        self.data[doc_id] = document
        return type('Result', (), {'inserted_id': doc_id})()
    
    async def find_one(self, query: Dict[str, Any] = None):
        """Find a single document"""
        if not query:
            return list(self.data.values())[0] if self.data else None
        
        for doc in self.data.values():
            if self._match_query(doc, query):
                return doc
        return None
    
    def find(self, query: Dict[str, Any] = None):
        """Find multiple documents"""
        if not query:
            return MemoryQuery(list(self.data.values()))
        
        matching_docs = []
        for doc in self.data.values():
            if self._match_query(doc, query):
                matching_docs.append(doc)
        
        return MemoryQuery(matching_docs)
    
    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any], upsert: bool = False):
        """Update a single document"""
        for doc_id, doc in self.data.items():
            if self._match_query(doc, query):
                if "$set" in update:
                    doc.update(update["$set"])
                if "$inc" in update:
                    for key, value in update["$inc"].items():
                        doc[key] = doc.get(key, 0) + value
                if "$addToSet" in update:
                    for key, value in update["$addToSet"].items():
                        if key not in doc:
                            doc[key] = []
                        if value not in doc[key]:
                            doc[key].append(value)
                if "$pull" in update:
                    for key, value in update["$pull"].items():
                        if key in doc and isinstance(doc[key], list):
                            doc[key] = [item for item in doc[key] if item != value]
                return
        
        if upsert:
            new_doc = {}
            if "$set" in update:
                new_doc.update(update["$set"])
            if "$inc" in update:
                for key, value in update["$inc"].items():
                    new_doc[key] = value
            await self.insert_one(new_doc)
    
    async def create_index(self, index_spec, unique: bool = False, sparse: bool = False):
        """Create index (no-op for memory database)"""
        pass
    
    def _match_query(self, doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
        """Simple query matching"""
        for key, value in query.items():
            if key == "_id":
                if doc.get("_id") != value:
                    return False
            elif key == "timestamp" and isinstance(value, dict):
                # Handle timestamp range queries
                doc_timestamp = doc.get("timestamp")
                if not doc_timestamp:
                    return False
                
                if "$gte" in value:
                    if doc_timestamp < value["$gte"]:
                        return False
                if "$lte" in value:
                    if doc_timestamp > value["$lte"]:
                        return False
            elif doc.get(key) != value:
                return False
        return True

class MemoryQuery:
    """Memory query result that mimics MongoDB cursor"""
    
    def __init__(self, documents: List[Dict[str, Any]]):
        self.documents = documents
    
    def sort(self, key: str, direction: int = 1):
        """Sort documents"""
        reverse = direction == -1
        self.documents.sort(key=lambda x: x.get(key, ""), reverse=reverse)
        return self
    
    def limit(self, count: int):
        """Limit number of documents"""
        self.documents = self.documents[:count]
        return self
    
    async def to_list(self, length: int = None):
        """Convert to list"""
        if length:
            return self.documents[:length]
        return self.documents
    
    def __aiter__(self):
        """Make async iterable"""
        return self
    
    async def __anext__(self):
        """Async iterator"""
        if not hasattr(self, '_index'):
            self._index = 0
        
        if self._index >= len(self.documents):
            raise StopAsyncIteration
        
        doc = self.documents[self._index]
        self._index += 1
        return doc

# Database configuration
USE_MEMORY_DB = os.getenv("USE_MEMORY_DB", "false").lower() == "true"
DATABASE_NAME = os.getenv("DATABASE_NAME", "teamwelly")

# Use in-memory database for development
database = None
users_collection = MemoryCollection("users")
user_sessions_collection = MemoryCollection("sessions")
programs_collection = MemoryCollection("programs")
user_progress_collection = MemoryCollection("user_progress")
chat_history_collection = MemoryCollection("chat_history")
payment_transactions_collection = MemoryCollection("payment_transactions")
user_behavior_collection = MemoryCollection("user_behavior")
challenges_collection = MemoryCollection("challenges")
bookings_collection = MemoryCollection("bookings")
notifications_collection = MemoryCollection("notifications")
wellness_packages_collection = MemoryCollection("wellness_packages")

async def init_database():
    """Initialize database with indexes and default data"""
    try:
        # Create indexes
        await users_collection.create_index("email", unique=True)
        await users_collection.create_index("google_id", unique=True, sparse=True)
        await user_sessions_collection.create_index("session_id", unique=True)
        await chat_history_collection.create_index("user_id")
        await user_behavior_collection.create_index("user_id")
        await payment_transactions_collection.create_index("session_id", unique=True)
        
        # Initialize default programs
        await init_default_programs()
        await init_default_challenges()
        
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

async def init_default_programs():
    """Initialize default wellness programs"""
    default_programs = [
        {
            "id": "stretch_mobility_1",
            "title": "Morning Neck & Shoulder Stretch",
            "category": "stretch_mobility",
            "duration": 5,
            "level": "beginner",
            "description": "Start your day with gentle neck and shoulder stretches",
            "instructions": [
                "Sit or stand with your spine straight",
                "Gently tilt your head to the right, hold for 15 seconds",
                "Repeat on the left side",
                "Roll your shoulders backwards 10 times"
            ],
            "benefits": ["Reduces neck tension", "Improves posture", "Increases mobility"],
            "video_url": "/videos/neck_shoulder_stretch.mp4",
            "thumbnail": "/images/neck_stretch.jpg"
        },
        {
            "id": "breath_stress_1",
            "title": "Box Breathing for Focus",
            "category": "breath_stress",
            "duration": 3,
            "level": "beginner",
            "description": "Calm your mind with structured breathing",
            "instructions": [
                "Inhale for 4 counts",
                "Hold for 4 counts",
                "Exhale for 4 counts",
                "Hold for 4 counts",
                "Repeat 8-10 times"
            ],
            "benefits": ["Reduces stress", "Improves focus", "Calms nervous system"],
            "video_url": "/videos/box_breathing.mp4",
            "thumbnail": "/images/breathing.jpg"
        },
        {
            "id": "mindset_growth_1",
            "title": "Mindful Moment Meditation",
            "category": "mindset_growth",
            "duration": 7,
            "level": "beginner",
            "description": "A quick mindfulness practice for mental clarity",
            "instructions": [
                "Find a comfortable seated position",
                "Close your eyes and breathe naturally",
                "Focus on your breath without changing it",
                "When thoughts arise, gently return to breath",
                "End with three deep breaths"
            ],
            "benefits": ["Reduces anxiety", "Improves focus", "Increases self-awareness"],
            "video_url": "/videos/mindful_moment.mp4",
            "thumbnail": "/images/meditation.jpg"
        },
        {
            "id": "strength_1",
            "title": "Core Stability Foundation",
            "category": "strength_foundations",
            "duration": 15,
            "level": "intermediate",
            "description": "Build a strong foundation with core exercises",
            "instructions": [
                "Start with a plank hold for 30 seconds",
                "Perform 10 dead bugs each side",
                "Hold side plank for 15 seconds each side",
                "Finish with 15 glute bridges"
            ],
            "benefits": ["Builds core strength", "Improves stability", "Prevents back pain"],
            "video_url": "/videos/core_stability.mp4",
            "thumbnail": "/images/core_strength.jpg"
        },
        {
            "id": "workplace_1",
            "title": "Desk Warrior Routine",
            "category": "workplace_wellness",
            "duration": 10,
            "level": "beginner",
            "description": "Perfect desk stretches for office workers",
            "instructions": [
                "Neck rolls - 5 in each direction",
                "Shoulder shrugs - 10 repetitions",
                "Wrist circles - 10 in each direction",
                "Seated spinal twist - hold 15 seconds each side",
                "Ankle circles - 10 in each direction"
            ],
            "benefits": ["Reduces office tension", "Improves posture", "Increases energy"],
            "video_url": "/videos/desk_routine.mp4",
            "thumbnail": "/images/desk_stretch.jpg"
        },
        {
            "id": "pain_performance_1",
            "title": "Lower Back Relief",
            "category": "pain_performance",
            "duration": 12,
            "level": "beginner",
            "description": "Targeted exercises for lower back pain relief",
            "instructions": [
                "Cat-cow stretches - 10 repetitions",
                "Knee-to-chest stretch - 30 seconds each leg",
                "Child's pose - hold for 1 minute",
                "Gentle hip circles - 10 in each direction"
            ],
            "benefits": ["Relieves back pain", "Improves flexibility", "Reduces stiffness"],
            "video_url": "/videos/back_relief.mp4",
            "thumbnail": "/images/back_pain.jpg"
        }
    ]
    
    for program in default_programs:
        await programs_collection.update_one(
            {"id": program["id"]}, 
            {"$set": program}, 
            upsert=True
        )

async def init_default_challenges():
    """Initialize default wellness challenges"""
    default_challenges = [
        {
            "id": "daily_stretch",
            "title": "Stretch 5 minutes today",
            "description": "Complete any stretch routine from our library",
            "type": "daily",
            "points": 50,
            "category": "stretch_mobility",
            "requirements": {"activity_type": "stretch", "duration": 5}
        },
        {
            "id": "breathing_session",
            "title": "Log a deep breath session",
            "description": "Practice breathing exercises for stress relief",
            "type": "daily",
            "points": 30,
            "category": "breath_stress",
            "requirements": {"activity_type": "breathing", "duration": 3}
        },
        {
            "id": "mindful_meditation",
            "title": "Complete a mindfulness session",
            "description": "Practice meditation for mental clarity",
            "type": "daily",
            "points": 40,
            "category": "mindset_growth",
            "requirements": {"activity_type": "meditation", "duration": 5}
        },
        {
            "id": "weekly_streak",
            "title": "Week-long wellness streak",
            "description": "Complete daily activities for 7 days in a row",
            "type": "weekly",
            "points": 200,
            "category": "general",
            "requirements": {"consecutive_days": 7}
        },
        {
            "id": "program_explorer",
            "title": "Try 3 different program categories",
            "description": "Explore variety in your wellness routine",
            "type": "weekly",
            "points": 150,
            "category": "general",
            "requirements": {"unique_categories": 3}
        }
    ]
    
    for challenge in default_challenges:
        await challenges_collection.update_one(
            {"id": challenge["id"]}, 
            {"$set": challenge}, 
            upsert=True
        )