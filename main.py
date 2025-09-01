from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from db import SessionLocal, engine, Base


app = FastAPI(title="Finance Tracker", version="0.1.0")

# Creates tables if they dont exists
Base.metadata.create_all(bind=engine)

# Opens up a db session for the request & closes it later
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Endpoints 
@app.post(
    "/transactions",
    response_model=schemas.TransactionOut,
    status_code=status.HTTP_201_CREATED)
def create_transaction(payload: schemas.TransactionCreate, db: Session = Depends(get_db)):
    tx = models.Transaction(**payload.model_dump())
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

@app.get("/transactions", response_model=List[schemas.TransactionOut])
def list_transactions(db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200),
                      offset: int = Query(0, ge=0)):
    rows = (
        db.query(models.Transaction)
        .order_by(models.Transaction.occured_on.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return rows

@app.get("/transactions/{tx_id}", response_model=schemas.TransactionOut)
def get_transaction(tx_id: int, db: Session = Depends(get_db)):
    tx = db.get(models.Transaction, tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail=f"Transaction with id:{tx_id} not found!")
    return tx

@app.put("/transactions/{tx_id}", response_model=schemas.TransactionOut)
def update_transaction(tx_id: int, payload: schemas.TransactionUpdate,
                       db: Session = Depends(get_db)):
    tx = db.get(models.Transaction, tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail=f"Transaction with id:{tx_id} not found!")
    
    changes = payload.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(tx, key, value)
    
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

@app.delete("/transactions/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(tx_id: int, db: Session = Depends(get_db)):
    tx = db.get(models.Transaction, tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail=f"Transaction with id:{tx_id} not found!")
    
    db.delete(tx)
    db.commit()

    return None


    







