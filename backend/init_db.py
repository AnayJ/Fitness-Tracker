"""Initialize database with schema."""
from app.db.database import engine, Base
from app.models.models import User, Meal, DailyLog

def init_db():
    """Initialize database."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
