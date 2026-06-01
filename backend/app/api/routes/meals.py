"""Meal routes."""
from fastapi import APIRouter, Depends, Header, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from app.db.database import get_db
from app.schemas.schemas import MealCreate, MealResponse, MealListResponse
from app.services.meal_service import MealService
from app.services.user_service import UserService
from app.core.security import decode_token

router = APIRouter(prefix="/meals", tags=["Meals"])


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


@router.post("/", response_model=MealResponse)
def create_meal(meal_data: MealCreate,
               db: Session = Depends(get_db),
               user = Depends(get_current_user)):
    """Create a new meal log."""
    meal = MealService.create_meal(db, user.id, meal_data)
    return MealResponse.from_orm(meal)


@router.get("/daily", response_model=MealListResponse)
def get_daily_meals(meal_date: date = Query(None),
                   db: Session = Depends(get_db),
                   user = Depends(get_current_user)):
    """Get meals for a specific date."""
    meals = MealService.get_daily_meals(db, user.id, meal_date)
    totals = MealService.calculate_daily_totals(meals)
    
    return MealListResponse(
        meals=[MealResponse.from_orm(m) for m in meals],
        total_calories=totals["total_calories"],
        total_protein=totals["total_protein"],
        total_carbs=totals["total_carbs"],
        total_fats=totals["total_fats"]
    )


@router.get("/{meal_id}", response_model=MealResponse)
def get_meal(meal_id: int,
            db: Session = Depends(get_db),
            user = Depends(get_current_user)):
    """Get a specific meal."""
    meal = MealService.get_meal_by_id(db, meal_id, user.id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    
    return MealResponse.from_orm(meal)


@router.put("/{meal_id}", response_model=MealResponse)
def update_meal(meal_id: int, meal_data: MealCreate,
               db: Session = Depends(get_db),
               user = Depends(get_current_user)):
    """Update a meal."""
    meal = MealService.update_meal(db, meal_id, user.id, meal_data)
    return MealResponse.from_orm(meal)


@router.delete("/{meal_id}")
def delete_meal(meal_id: int,
               db: Session = Depends(get_db),
               user = Depends(get_current_user)):
    """Delete a meal."""
    if not MealService.delete_meal(db, meal_id, user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    
    return {"message": "Meal deleted successfully"}
