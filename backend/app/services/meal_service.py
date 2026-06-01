"""Meal service for meal management."""
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.models import Meal, DailyLog
from app.schemas.schemas import MealCreate, MealResponse


class MealService:
    """Service for meal operations."""
    
    @staticmethod
    def create_meal(db: Session, user_id: int, meal_data: MealCreate) -> Meal:
        """Create a new meal."""
        meal = Meal(
            user_id=user_id,
            name=meal_data.name,
            description=meal_data.description,
            calories=meal_data.calories,
            protein=meal_data.protein,
            carbs=meal_data.carbs,
            fats=meal_data.fats,
            meal_date=datetime.utcnow()
        )
        db.add(meal)
        db.commit()
        db.refresh(meal)
        return meal
    
    @staticmethod
    def get_daily_meals(db: Session, user_id: int, meal_date: date = None) -> list:
        """Get all meals for a specific date."""
        if meal_date is None:
            meal_date = date.today()
        
        start_of_day = datetime.combine(meal_date, datetime.min.time())
        end_of_day = datetime.combine(meal_date, datetime.max.time())
        
        meals = db.query(Meal).filter(
            and_(
                Meal.user_id == user_id,
                Meal.meal_date >= start_of_day,
                Meal.meal_date <= end_of_day
            )
        ).all()
        return meals
    
    @staticmethod
    def calculate_daily_totals(meals: list) -> dict:
        """Calculate daily totals from meal list."""
        return {
            "total_calories": sum(m.calories for m in meals),
            "total_protein": sum(m.protein for m in meals),
            "total_carbs": sum(m.carbs for m in meals),
            "total_fats": sum(m.fats for m in meals)
        }
    
    @staticmethod
    def get_meal_by_id(db: Session, meal_id: int, user_id: int) -> Meal:
        """Get meal by ID."""
        return db.query(Meal).filter(
            and_(Meal.id == meal_id, Meal.user_id == user_id)
        ).first()
    
    @staticmethod
    def delete_meal(db: Session, meal_id: int, user_id: int) -> bool:
        """Delete a meal."""
        meal = MealService.get_meal_by_id(db, meal_id, user_id)
        if not meal:
            return False
        
        db.delete(meal)
        db.commit()
        return True
    
    @staticmethod
    def update_meal(db: Session, meal_id: int, user_id: int, meal_data: MealCreate) -> Meal:
        """Update a meal."""
        meal = MealService.get_meal_by_id(db, meal_id, user_id)
        if not meal:
            raise ValueError("Meal not found")
        
        meal.name = meal_data.name
        meal.description = meal_data.description
        meal.calories = meal_data.calories
        meal.protein = meal_data.protein
        meal.carbs = meal_data.carbs
        meal.fats = meal_data.fats
        
        db.add(meal)
        db.commit()
        db.refresh(meal)
        return meal
