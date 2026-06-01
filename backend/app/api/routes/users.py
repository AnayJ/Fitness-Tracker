"""User routes."""
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import UserResponse, UserProfile, UserOnboarding, AIGoalResponse
from app.services.user_service import UserService
from app.services.ai_service import AIService
from app.core.security import decode_token
from app.utils.calculators import calculate_bmi, calculate_maintenance_calories, estimate_weight_change

router = APIRouter(prefix="/users", tags=["Users"])


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Dependency to get current user from token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token required")
    
    token = authorization[7:]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user


@router.get("/profile", response_model=UserResponse)
def get_profile(user = Depends(get_current_user)):
    """Get user profile."""
    return UserResponse.from_orm(user)


@router.put("/profile", response_model=UserResponse)
def update_profile(profile_data: UserProfile, 
                   db: Session = Depends(get_db),
                   user = Depends(get_current_user)):
    """Update user profile."""
    updated_user = UserService.update_profile(db, user.id, profile_data)
    return UserResponse.from_orm(updated_user)


@router.post("/onboarding", response_model=UserResponse)
def complete_onboarding(onboarding_data: UserOnboarding,
                       db: Session = Depends(get_db),
                       user = Depends(get_current_user)):
    """Complete user onboarding."""
    bmi = calculate_bmi(onboarding_data.weight, onboarding_data.height)
    maintenance = calculate_maintenance_calories(onboarding_data.weight, onboarding_data.height)
    
    # Determine target calories
    if onboarding_data.fitness_goal == "lose":
        target_calories = maintenance * 0.85
    elif onboarding_data.fitness_goal == "gain":
        target_calories = maintenance * 1.15
    else:
        target_calories = maintenance
    
    updated_user = UserService.complete_onboarding(
        db, user.id,
        onboarding_data.weight,
        onboarding_data.height,
        onboarding_data.fitness_goal,
        target_calories
    )
    
    return UserResponse.from_orm(updated_user)


@router.post("/suggest-goal", response_model=AIGoalResponse)
def suggest_goal(weight: float, height: float, 
                db: Session = Depends(get_db),
                user = Depends(get_current_user)):
    """Get AI suggested fitness goal."""
    bmi = calculate_bmi(weight, height)
    maintenance = calculate_maintenance_calories(weight, height)
    
    suggestion = AIService.suggest_fitness_goal(bmi, maintenance, weight, height)
    
    return AIGoalResponse(
        suggested_goal=suggestion["suggested_goal"],
        explanation=suggestion["explanation"],
        target_calories=suggestion["target_calories"],
        weekly_projection=suggestion["weekly_projection"]
    )
