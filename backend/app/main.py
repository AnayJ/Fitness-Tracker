"""Main FastAPI application."""
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.models.models import User, Meal, DailyLog
from app.api.routes import auth, users, meals, dashboard, ai
from app.core.config import settings

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Fitness Tracker API",
    description="A comprehensive fitness tracking application with AI integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Fitness Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# Middleware to extract token from header
@app.middleware("http")
async def add_token_to_request(request, call_next):
    """Extract Bearer token from Authorization header."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        request.scope["token"] = token
    response = await call_next(request)
    return response


# Include routers with token dependency
def get_token_from_header(authorization: str = Header(None)):
    """Extract token from header."""
    if authorization and authorization.startswith("Bearer "):
        return authorization[7:]
    return None


# Re-include routers with updated dependencies
auth_router = auth.router
users_router = users.router
meals_router = meals.router
dashboard_router = dashboard.router
ai_router = ai.router

# Override the get_current_user dependencies
from fastapi import Depends

def users_get_current_user(token: str = Depends(get_token_from_header), db = Depends()):
    from app.db.database import get_db
    db = next(get_db())
    return users.get_current_user(token, db)

def meals_get_current_user(token: str = Depends(get_token_from_header), db = Depends()):
    from app.db.database import get_db
    db = next(get_db())
    return meals.get_current_user(token, db)

def dashboard_get_current_user(token: str = Depends(get_token_from_header), db = Depends()):
    from app.db.database import get_db
    db = next(get_db())
    return dashboard.get_current_user(token, db)

def ai_get_current_user(token: str = Depends(get_token_from_header), db = Depends()):
    from app.db.database import get_db
    db = next(get_db())
    return ai.get_current_user(token, db)

app.include_router(users_router)
app.include_router(meals_router)
app.include_router(dashboard_router)
app.include_router(ai_router)


@app.exception_handler(Exception)
def general_exception_handler(request, exc):
    """Handle general exceptions."""
    return {
        "detail": str(exc)
    }
