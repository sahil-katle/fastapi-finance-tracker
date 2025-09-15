from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from settings import settings

import models, schemas
from db import SessionLocal
from security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

# --- DB dependency (kept local for now; we'll refactor later) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This will make swagger show a token box in Authorize pop-up
bearer_scheme = HTTPBearer()

@router.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def signup(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user with this email already exists 
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the incoming plain password
    hashed_pw = hash_password(payload.password)

    # Create the ORM object with hashed password 
    user = models.User(email=payload.email, hashed_password= hashed_pw)

    #Save to db 
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    1) Find user by email
    2) Verify password (bcrypt)
    3) Create & return JWT access token
    """
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # user.id goes in "sub" claim
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# --- Decode the JWT and return the current user ---
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),) -> models.User:

    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user = db.get(models.User, int(sub))
    if not user or not user.is_active:
        raise HTTPException(401, "Inactive or missing user")
    return user

# (Optional) test endpoint to verify auth works
@router.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user

