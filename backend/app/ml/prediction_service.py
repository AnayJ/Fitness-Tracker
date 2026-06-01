"""ML service for calorie predictions."""
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import Meal
from sqlalchemy import and_


class CaloriePredictionService:
    """Service for predicting calorie consumption."""
    
    @staticmethod
    def predict_daily_total(db: Session, user_id: int, target_calories: float, 
                           current_hour: int = None) -> dict:
        """Predict if user will exceed daily calorie target.
        
        Args:
            db: Database session
            user_id: User ID
            target_calories: Daily calorie target
            current_hour: Current hour (0-23), defaults to now
            
        Returns:
            Prediction dictionary with probability and projected total
        """
        if current_hour is None:
            current_hour = datetime.utcnow().hour
        
        # Get today's meals
        today = datetime.utcnow().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        current_time = datetime.utcnow()
        
        meals = db.query(Meal).filter(
            and_(
                Meal.user_id == user_id,
                Meal.meal_date >= start_of_day,
                Meal.meal_date <= current_time
            )
        ).all()
        
        current_calories = sum(m.calories for m in meals)
        
        # Simple linear prediction: current rate * remaining hours
        hours_passed = current_hour
        hours_remaining = 24 - hours_passed
        
        if hours_passed == 0:
            # No data yet, assume uniform distribution
            projected_total = target_calories
        else:
            hourly_rate = current_calories / max(hours_passed, 1)
            projected_total = current_calories + (hourly_rate * hours_remaining)
        
        will_exceed = projected_total > target_calories
        confidence = min(100, (hours_passed / 24) * 100)
        
        return {
            "current_calories": round(current_calories, 0),
            "projected_total": round(projected_total, 0),
            "target_calories": target_calories,
            "remaining_calories": round(target_calories - current_calories, 0),
            "will_exceed": will_exceed,
            "exceeded_by": round(projected_total - target_calories, 0) if will_exceed else 0,
            "confidence": round(confidence, 1),
            "meals_logged": len(meals)
        }
    
    @staticmethod
    def get_weekly_trend(db: Session, user_id: int) -> dict:
        """Get weekly calorie consumption trend.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Dictionary with daily totals for past 7 days
        """
        daily_totals = {}
        
        for i in range(7):
            date = datetime.utcnow().date() - timedelta(days=i)
            start_of_day = datetime.combine(date, datetime.min.time())
            end_of_day = datetime.combine(date, datetime.max.time())
            
            meals = db.query(Meal).filter(
                and_(
                    Meal.user_id == user_id,
                    Meal.meal_date >= start_of_day,
                    Meal.meal_date <= end_of_day
                )
            ).all()
            
            daily_totals[date.isoformat()] = sum(m.calories for m in meals)
        
        return daily_totals
