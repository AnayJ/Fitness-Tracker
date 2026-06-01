"""Dashboard routes."""
from fastapi import APIRouter, Depends, Header, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from app.db.database import get_db
from app.schemas.schemas import DashboardSummary, MealResponse
from app.services.meal_service import MealService
from app.services.user_service import UserService
from app.services.ai_service import AIService
from app.ml.prediction_service import CaloriePredictionService
from app.core.security import decode_token

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


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


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(meal_date: date = Query(None),
                         db: Session = Depends(get_db),
                         user = Depends(get_current_user)):
    """Get dashboard summary for a date."""
    meals = MealService.get_daily_meals(db, user.id, meal_date)
    totals = MealService.calculate_daily_totals(meals)
    
    target_calories = user.target_calories or 2000
    remaining = target_calories - totals["total_calories"]
    
    # Get prediction
    prediction = CaloriePredictionService.predict_daily_total(
        db, user.id, target_calories
    )
    
    return DashboardSummary(
        date=meal_date or date.today(),
        target_calories=target_calories,
        consumed_calories=totals["total_calories"],
        remaining_calories=max(0, remaining),
        protein=totals["total_protein"],
        carbs=totals["total_carbs"],
        fats=totals["total_fats"],
        meal_count=len(meals),
        meals=[MealResponse.from_orm(m) for m in meals],
        exceeded=totals["total_calories"] > target_calories,
        prediction=prediction
    )


@router.get("/weekly-report")
def get_weekly_report(db: Session = Depends(get_db),
                     user = Depends(get_current_user)):
    """Get weekly health report."""
    from datetime import datetime, timedelta
    
    # Calculate weekly summary
    daily_totals = {}
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0
    days_tracked = 0
    
    for i in range(7):
        check_date = date.today() - timedelta(days=i)
        meals = MealService.get_daily_meals(db, user.id, check_date)
        
        if meals:
            days_tracked += 1
            totals = MealService.calculate_daily_totals(meals)
            daily_totals[check_date.isoformat()] = totals
            total_calories += totals["total_calories"]
            total_protein += totals["total_protein"]
            total_carbs += totals["total_carbs"]
            total_fats += totals["total_fats"]
    
    avg_calories = total_calories / max(days_tracked, 1)
    avg_protein = total_protein / max(days_tracked, 1)
    avg_carbs = total_carbs / max(days_tracked, 1)
    avg_fats = total_fats / max(days_tracked, 1)
    
    summary = {
        "days_tracked": days_tracked,
        "avg_calories": avg_calories,
        "avg_protein": avg_protein,
        "avg_carbs": avg_carbs,
        "avg_fats": avg_fats,
        "target_calories": user.target_calories or 2000,
        "daily_breakdown": daily_totals
    }
    
    user_data = {
        "name": user.name,
        "fitness_goal": user.fitness_goal,
        "target_calories": user.target_calories
    }
    
    report = AIService.generate_weekly_report(user_data, summary)
    
    return {
        "report": report,
        "summary": summary
    }


@router.get("/prediction")
def get_calorie_prediction(db: Session = Depends(get_db),
                          user = Depends(get_current_user)):
    """Get calorie prediction for today."""
    target_calories = user.target_calories or 2000
    prediction = CaloriePredictionService.predict_daily_total(db, user.id, target_calories)
    
    return prediction


@router.get("/weekly-trend")
def get_weekly_trend(db: Session = Depends(get_db),
                    user = Depends(get_current_user)):
    """Get weekly calorie trend."""
    trend = CaloriePredictionService.get_weekly_trend(db, user.id)
    
    return {
        "trend": trend,
        "target_calories": user.target_calories or 2000
    }
