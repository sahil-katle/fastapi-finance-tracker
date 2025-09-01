# Personal Notes 

## db.py file 

- SQLAlchemy -> ORM (Object relational mapper) -> lets us write Python classes instead of raw SQL 
- create_engine -> sets up the connection to the db 
- SQLALCHEMY_DATABASE_URL -> db connection string  (Need to change this URL if I cange the db later eg: MYSql )

- SessionLocal -> makes short-lived db connection as per request
- Base -> its the class which we need to inherit when we create models/tables. A parent class for my models so SQLAlchemy knows "This is a table"

## Models.py 
- This is nothing but the Python class that represents tables in the db.

- Eg: Ask: What is the one “thing” my app must store first?
In a finance tracker, it’s a Transaction.

- List the minimum details you need about it.
ID (unique identifier)
Description (what it’s about: “Coffee”, “Salary”)
Amount (how much money)
Kind (is it “income” or “expense”)
Category (like “Food”, “Rent”)
Date (when it happened)
Note (optional long text)

# Notes: SQLAlchemy Models Basics

### Why use `index=True`?
- Creates a **database index** on that column.
- Index = like a **table of contents** in a book → makes lookups faster.
- Without index: DB scans all rows.
- With index: DB can jump directly to matching rows.
⚠️ Don’t overuse indexes → they speed up reads but slow down writes a little.

---
### created_at & updated_at - arguments and why they are needed?
- DateTime(timezone=True) → store both date + time with timezone info.
- server_default=func.now()
Database sets this automatically to the current time when row is created.
Example: when you insert a transaction, DB fills created_at.
- onupdate=func.now()
Special for updated_at.
Updates to NOW() automatically every time the row is updated.
- nullable=False
Column must always have a value (can’t be empty).

# Schemas.py basics 

## What is schema 
A schema is the translator between DB-World & API-World:
It validates input (ensures the JSON has the right fields, right types, no junk).
It defines output

## Why do we need them ? 

✅ Validation: If someone tries to send "amount": "abc", Pydantic schema will reject it → 422 Unprocessable Entity.
✅ Clarity: Defines what exactly goes in/out of each endpoint.
✅ Security: Stops you from accidentally returning sensitive DB columns (like hashed passwords).
✅ Docs: FastAPI uses schemas to auto-generate Swagger docs.

## Creating schemas.py file

- BaseModel -> Parent class for all schemas 
- Field() -> lets us add rules 
- Literal -> Restricts value to certain options only
 eg: kind column can only have 2 values [income, expense]


- Ellipsis (...) -> This means the field is required 

### Class Config 
from_attributes = True -> Tells pydantic that you are allowed to read objects and not just plain dict

eg: Pydantic expects dict when creating schema. But usually in projects, we'll often have SQLAlchemy objects instead of dict. 

# Creating endpoints 

## What is an endpoint?
- Specific URL in our API which the client can call 
- Each endpoint is tied to one specifc HTTP method and does one clear jog
eg: POOST, PUT, GET, DELETE

- `/transactions` (POST) -> Create a transaction 
- `/transactions` (GET) -> List all transactions 

## Why are they important ?
- They are named **doors** with whihc cliets interact with our backend 
(They dont care about models & dbs)
- They just talk to endpoints using HTTP + JSON 
- Good endpoints follow REST conventions 
    - **Resources** are nouns like transactiona, users, groups 
    - **Methods** define actions like GET -> read, POST -> create, etc.

✅ **Think of endpoints like doors into your app’s features.**  
Each door has a label (path), a lock (method), and rules (schemas + status codes).


# ORM (Object Relation Mapper)
- Lets us interact with the db using objects instead of writing raw sql.
- In Python -> SQLAlchemy is the most common ORM 

### DB interaction
- Uses **SQLAlchemy ORM** (Object Relational Mapper):
  - `db.query(Transaction)` → SELECT * FROM transactions
  - `.order_by(occurred_on DESC)` → newest first
  - `.limit(limit)` → cap number of rows
  - `.offset(offset)` → skip rows
- `.all()` → returns a list of Transaction objects.
