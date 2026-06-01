"""User service for authentication and user management."""
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.schemas import UserRegister, UserProfile, UserResponse
from app.core.security import get_password_hash, verify_password
from app.utils.calculators import calculate_bmi, calculate_maintenance_calories


class UserService:
    """Service for user operations."""
    
    @staticmethod
    def create_user(db: Session, user_data: UserRegister) -> User:
        """Create a new user."""
        # Check if user exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create new user
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=get_password_hash(user_data.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def verify_password(db: Session, email: str, password: str) -> User:
        """Verify user credentials."""
        user = UserService.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password):
            return None
        return user
    
    @staticmethod
    def update_profile(db: Session, user_id: int, profile_data: UserProfile) -> User:
        """Update user profile."""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        if profile_data.weight is not None:
            user.weight = profile_data.weight
        if profile_data.height is not None:
            user.height = profile_data.height
        
        # Calculate BMI if both weight and height are available
        if user.weight and user.height:
            user.bmi = calculate_bmi(user.weight, user.height)
            user.maintenance_calories = calculate_maintenance_calories(
                weight=user.weight,
                height=user.height
            )
        
        if profile_data.fitness_goal is not None:
            user.fitness_goal = profile_data.fitness_goal
            # Set target calories based on goal
            if user.maintenance_calories:
                if profile_data.fitness_goal == "lose":
                    user.target_calories = user.maintenance_calories * 0.85  # 15% deficit
                elif profile_data.fitness_goal == "gain":
                    user.target_calories = user.maintenance_calories * 1.15  # 15% surplus
                else:  # maintain
                    user.target_calories = user.maintenance_calories
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def complete_onboarding(db: Session, user_id: int, weight: float, height: float, 
                           fitness_goal: str, target_calories: float) -> User:
        """Complete user onboarding."""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        user.weight = weight
        user.height = height
        user.bmi = calculate_bmi(weight, height)
        user.maintenance_calories = calculate_maintenance_calories(weight, height)
        user.fitness_goal = fitness_goal
        user.target_calories = target_calories
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
