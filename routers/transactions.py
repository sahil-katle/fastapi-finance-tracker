# routers/transactions.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_  # Helps build OR condition in SQLAlchemy
from datetime import date
from routers.auth import get_current_user

import models, schemas
from db import SessionLocal

router = APIRouter(prefix="/transactions", tags=["transactions"])

# --- DB dependency (kept local for now; we'll refactor later) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- CREATE ----------
@router.post("", response_model=schemas.TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: schemas.TransactionCreate, 
                       db: Session = Depends(get_db), 
                       current_user=Depends(get_current_user)
                       ):
    tx = models.Transaction(user_id=current_user.id, **payload.model_dump())
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

# ---------- LIST ----------
@router.get("", response_model=schemas.TransactionListOut)
def list_transactions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    # pagination
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    # Filters (all optional)
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    kind: Optional[str] = Query(None, pattern="^(income|expense)$"),
    category: Optional[str] = Query(None),
    q: Optional[str] = Query(None, description="Search in description or note"),
    min_amount: Optional[float] = Query(None, gt=0),
    max_amount: Optional[float] = Query(None, gt=0),
):
    query = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id)

    #apply filters if provided
    if start_date:
        query = query.filter(models.Transaction.occured_on >= start_date)
    if end_date:
        query = query.filter(models.Transaction.occured_on >= end_date)
    if kind:
        query = query.filter(models.Transaction.kind == kind)
    if category:
        query = query.filter(models.Transaction.category == category)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                models.Transaction.description.ilike(like),
                models.Transaction.note.ilike(like),
            )
        )
    if min_amount:
        query = query.filter(models.Transaction.amount >= min_amount)
    if max_amount:
        query = query.filter(models.Transaction.amount <= max_amount)

    total = query.count()

    rows = (
        query.order_by(models.Transaction.occured_on.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return {
        "items": rows,
        "total": total, 
        "limit": limit,
        "offset": offset
    }
    

# ---------- GET ONE ----------
@router.get("/{tx_id}", response_model=schemas.TransactionOut)
def get_transaction(tx_id: int, db: Session = Depends(get_db),
                    current_user=Depends(get_current_user)):
    tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id,
                                           models.Transaction.user_id == current_user.id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx

# ---------- UPDATE ----------
@router.put("/{tx_id}", response_model=schemas.TransactionOut)
def update_transaction(tx_id: int, payload: schemas.TransactionUpdate, db: Session = Depends(get_db), current_user= Depends(get_current_user)):
    tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id, models.Transaction.user_id == current_user.id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    changes = payload.model_dump(exclude_unset=True)  # only fields the client sent
    for k, v in changes.items():
        setattr(tx, k, v)

    # db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

# ---------- DELETE ----------
@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(tx_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id, models.Transaction.user_id == current_user.id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(tx)
    db.commit()
    return None
