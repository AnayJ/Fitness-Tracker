"""AI routes."""
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import ChatRequest, ChatResponse
from app.services.ai_service import AIService
from app.services.user_service import UserService
from app.core.security import decode_token

router = APIRouter(prefix="/ai", tags=["AI"])


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


@router.post("/chat", response_model=ChatResponse)
def fitness_chat(request: ChatRequest,
                db: Session = Depends(get_db),
                user = Depends(get_current_user)):
    """Chat with fitness AI assistant."""
    user_data = {
        "name": user.name,
        "fitness_goal": user.fitness_goal,
        "target_calories": user.target_calories,
        "weight": user.weight,
        "height": user.height,
        "bmi": user.bmi
    }
    
    response = AIService.chat(request.message, user_data, request.history)
    
    return ChatResponse(
        response=response,
        suggested_action=None
    )
