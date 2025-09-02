from fastapi import FastAPI
from routers.transactions import router as transactions_router

import models, schemas
from db import engine, Base


app = FastAPI(title="Finance Tracker", version="0.1.0")

# Creates tables if they dont exists
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

# mount transactions endpoints
app.include_router(transactions_router)