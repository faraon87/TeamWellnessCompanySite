from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "teamwelly")

# MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

# Collections
users_collection = database["users"]
sessions_collection = database["sessions"]
programs_collection = database["programs"]
user_progress_collection = database["user_progress"]
chat_history_collection = database["chat_history"]
payment_transactions_collection = database["payment_transactions"]
user_behavior_collection = database["user_behavior"]
challenges_collection = database["challenges"]
bookings_collection = database["bookings"]
notifications_collection = database["notifications"]

async def init_database():
    """Initialize database with indexes and default data"""
    try:
        # Create indexes
        await users_collection.create_index("email", unique=True)
        await users_collection.create_index("google_id", unique=True, sparse=True)
        await sessions_collection.create_index("session_id", unique=True)
        await chat_history_collection.create_index([("user_id", 1), ("timestamp", -1)])
        await user_behavior_collection.create_index([("user_id", 1), ("timestamp", -1)])
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
            "id": "weekly_streak",
            "title": "Week-long wellness streak",
            "description": "Complete daily activities for 7 days in a row",
            "type": "weekly",
            "points": 200,
            "category": "general",
            "requirements": {"consecutive_days": 7}
        }
    ]
    
    for challenge in default_challenges:
        await challenges_collection.update_one(
            {"id": challenge["id"]}, 
            {"$set": challenge}, 
            upsert=True
        )