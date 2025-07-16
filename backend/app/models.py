from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    INDIVIDUAL = "individual"
    CORPORATE = "corporate"
    ADMIN = "admin"

class UserPlan(str, Enum):
    BASIC = "basic"
    PLUS = "plus"
    PREMIUM = "premium"

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    name: str
    avatar: Optional[str] = None
    role: UserRole = UserRole.INDIVIDUAL
    plan: UserPlan = UserPlan.BASIC
    google_id: Optional[str] = None
    company_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    onboarding_completed: bool = False
    selected_goals: List[str] = []
    assessment_data: Dict[str, Any] = {}
    device_integrations: List[str] = []
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSignup(BaseModel):
    email: EmailStr
    name: str
    plan: UserPlan = UserPlan.BASIC
    company_code: Optional[str] = None

class GoogleAuthRequest(BaseModel):
    access_token: str

class UserProgress(BaseModel):
    user_id: str
    daily_completion: float = 0.0
    weekly_completion: float = 0.0
    monthly_completion: float = 0.0
    welly_points: int = 0
    current_streak: int = 0
    completed_programs: List[str] = []
    bookmarked_programs: List[str] = []
    completed_challenges: List[str] = []
    last_activity: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ChatMessage(BaseModel):
    user_id: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_insights: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[str]] = None

class UserBehavior(BaseModel):
    user_id: str
    action: str
    page: str
    details: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None

class Program(BaseModel):
    id: str
    title: str
    category: str
    duration: int  # in minutes
    level: str
    description: str
    instructions: List[str]
    benefits: List[str]
    video_url: Optional[str] = None
    thumbnail: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Challenge(BaseModel):
    id: str
    title: str
    description: str
    type: str  # daily, weekly, monthly
    points: int
    category: str
    requirements: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Booking(BaseModel):
    id: Optional[str] = None
    user_id: str
    coach_id: str
    session_type: str  # 1-on-1, group
    date: datetime
    duration: int  # in minutes
    status: str = "scheduled"  # scheduled, completed, cancelled
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentTransaction(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: str
    amount: float
    currency: str = "usd"
    status: str = "initiated"  # initiated, completed, failed, cancelled
    payment_status: str = "pending"  # pending, paid, failed
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentRequest(BaseModel):
    package_id: str
    success_url: str
    cancel_url: str
    metadata: Optional[Dict[str, Any]] = {}

class WellnessPackage(BaseModel):
    id: str
    name: str
    description: str
    price: float
    features: List[str]
    duration: str  # monthly, yearly
    stripe_price_id: Optional[str] = None

# Wellness packages configuration
WELLNESS_PACKAGES = {
    "basic": WellnessPackage(
        id="basic",
        name="Basic Plan",
        description="Essential wellness content",
        price=9.99,
        features=[
            "Access to all programs",
            "Progress tracking",
            "Basic challenges",
            "Community support"
        ],
        duration="monthly"
    ),
    "plus": WellnessPackage(
        id="plus",
        name="Plus Plan",
        description="Everything in Basic plus group coaching",
        price=19.99,
        features=[
            "Everything in Basic",
            "Group coaching sessions",
            "Advanced challenges",
            "Wellness analytics",
            "Device integrations"
        ],
        duration="monthly"
    ),
    "premium": WellnessPackage(
        id="premium",
        name="Premium Plan",
        description="Complete wellness solution",
        price=39.99,
        features=[
            "Everything in Plus",
            "1-on-1 coaching sessions",
            "Custom wellness plans",
            "Priority support",
            "Advanced analytics"
        ],
        duration="monthly"
    )
}