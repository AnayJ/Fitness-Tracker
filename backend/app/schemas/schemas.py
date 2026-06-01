"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ============== User Schemas ==============
class UserRegister(BaseModel):
    """User registration request."""
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class UserProfile(BaseModel):
    """User profile update request."""
    weight: Optional[float] = None
    height: Optional[float] = None
    fitness_goal: Optional[str] = None  # "lose", "gain", "maintain"


class UserOnboarding(BaseModel):
    """User onboarding data."""
    weight: float  # in kg
    height: float  # in cm
    fitness_goal: str  # "lose", "gain", "ask_ai"
    

class UserResponse(BaseModel):
    """User response model."""
    id: int
    name: str
    email: str
    weight: Optional[float]
    height: Optional[float]
    bmi: Optional[float]
    maintenance_calories: Optional[float]
    fitness_goal: Optional[str]
    target_calories: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== Authentication Schemas ==============
class Token(BaseModel):
    """Token response."""
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    """Token data payload."""
    user_id: Optional[int] = None


# ============== Meal Schemas ==============
class MealCreate(BaseModel):
    """Create meal request."""
    name: str
    description: Optional[str] = None
    calories: float
    protein: float
    carbs: float
    fats: float


class MealResponse(BaseModel):
    """Meal response model."""
    id: int
    user_id: int
    name: str
    description: Optional[str]
    calories: float
    protein: float
    carbs: float
    fats: float
    meal_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class MealListResponse(BaseModel):
    """List of meals response."""
    meals: List[MealResponse]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float


# ============== Dashboard Schemas ==============
class DashboardSummary(BaseModel):
    """Daily dashboard summary."""
    date: datetime
    target_calories: float
    consumed_calories: float
    remaining_calories: float
    protein: float
    carbs: float
    fats: float
    meal_count: int
    meals: List[MealResponse]
    exceeded: bool
    prediction: Optional[dict] = None  # ML prediction data


class CalorieGoal(BaseModel):
    """Calorie goal data."""
    fitness_goal: str
    target_calories: float
    weekly_projection: str


# ============== AI Schemas ==============
class AIGoalSuggestion(BaseModel):
    """AI goal suggestion request."""
    weight: float
    height: float
    bmi: float
    maintenance_calories: float


class AIGoalResponse(BaseModel):
    """AI goal suggestion response."""
    suggested_goal: str
    explanation: str
    target_calories: float
    weekly_projection: str


class ChatMessage(BaseModel):
    """Chat message."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Chat request."""
    message: str
    history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    """Chat response."""
    response: str
    suggested_action: Optional[str] = None
