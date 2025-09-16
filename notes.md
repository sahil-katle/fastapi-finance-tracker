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

# Routers in Fastapi 
In FastAPI, a **router** is a way to group related endpoints together.
- Instead of keeping all routes in `main.py`, you split them by feature/module.

## How to Define a Router
1. Import and create a router instance:
   ```python
   from fastapi import APIRouter

   router = APIRouter(
       prefix="/transactions",   # all endpoints start with /transactions
       tags=["transactions"]     # label in Swagger UI
   )
  
# Advanced GET/Transactions (Query Parameters filtering)
- Usual practice to narrow the results 

- Filters like "Show only expenses" OR "Show items between specific dates" 

## Pagination Envelope / Response Envelope 
- Instead of returning a bare list, we are returning JSON object with metadata + items.

eg:
```
 {
  "items": [...],
  "total": 42,
  "limit": 10,
  "offset": 0
}
```

- For this first create a new response envelope schema which will have the list of ites, total, limit & offset


# Authentication

- We will use ```pip install "passlib[bcrypt]"```

- bcrypt is a strong hashing algorithm -> passwords are never stored in plaintext or reversible form -> Basically on login, bcrypt verifies the submitted password with stored hash. 

## Security.py 
- We declare the context manager for hashing as well as 2 function - one to hash the passswords and other to verify the password. 

## Schemas.py
- Created 2 more schemas.
- for userCreate which will be used -> Request body when a new user signs up (POST /auth/signup) 
- for UserOut -> Request body when a new user signs up (POST /auth/signup)

## User Model & Schemas
- **User model (SQLAlchemy):**
  - `id`, `email` (unique), `hashed_password`, `is_active`.
- **Schemas:**
  - `UserCreate` → request body for signup (`{ email, password }`).
  - `UserOut` → safe response (returns `{ id, email }`, never password).
  - `Token` → response for login (`{ access_token, token_type }`).

## Signup Flow (`POST /auth/signup`)
1. Client sends `{ email, password }`.
2. API:
   - Validates email with `EmailStr`.
   - Checks if email already exists.
   - Hashes password with bcrypt.
   - Stores user with `hashed_password`.
3. Returns `UserOut` (id + email).

---

## Login Flow (`POST /auth/login`)
1. Client sends `{ email, password }`.
2. API:
   - Finds user by email.
   - Verifies plain password vs hashed password.
   - If valid → creates **JWT access token** with user id in `sub`.
3. Returns `{ access_token, token_type: "bearer" }`.

# ---JWT--------

# JWT (JSON Web Token)

## What is JWT?
- JWT is just a **string** (a token) that proves who you are.
- Think of it like a **movie ticket**:
  - It has your name/seat (data inside).
  - It’s signed/stamped so the cinema knows it’s valid.
  - You don’t log in at the counter again — just show the ticket.

---

## Why do we need JWT?
- Without tokens: the server would have to **remember every user** that logged in (sessions in memory).  
- With JWT: the **token itself carries the proof** → server doesn’t store anything extra.  
- Client includes the token in every request → server checks it quickly.

---

## Naive Example

### Without JWT
1. You sign in → server remembers `you = logged_in` in memory.
2. Every time you ask for `/transactions`, server checks its memory to see if you’re logged in.
3. If the server restarts, memory is wiped → you’re logged out everywhere.

### With JWT
1. You sign in → server gives you a **token** (like `eyJhbGciOi...`).
2. This token says: `"sub": 1` (you are user with id=1) and `"exp": "in 12 hours"`.
3. You store this token in your client (browser, mobile app).
4. Every request → you send: Authorization: Bearer <token> 

5. Server just:
- Checks the signature (is it real?).
- Reads `sub = 1` → knows you’re user 1.
- Doesn’t need to remember anything else.

---

## In Our App (Finance Tracker)
- On **login**: we create a JWT with:
- `sub`: user id  
- `exp`: expiry time
- On each request:
- Swagger (or your frontend) attaches the token.
- `get_current_user` decodes it.
- Server instantly knows *which user is calling*.

---

## Benefits
- **Stateless** → server doesn’t store sessions.
- **Secure** → signed with secret key, cannot be forged.
- **Portable** → works in Swagger, Postman, frontend apps.
- **Scoped** → each user’s data is kept separate using their `sub` (id) from the token.

## Access protected endpoints 
- get_current_user = ticket checker 🛂
- Makes sure the JWT is valid and belongs to a real user.
- Returns that user → so endpoints know who is calling.
- Will be added to every protected endpoint in the future.


--------------------------------------------------------------------


# **Connecting Transactions and Users model**

- Open models.py and add a foreign key on the Transaction table. This establishes one-to-many relationship:
**One user → many transactions**

- Ensures every transaction is linked to a user 

## What we did for Access-Protected Endpoints
- Added security layers so only valid users can access certain API routes.
Process:
- User authentication → check credentials (e.g., email + password) and issue a token.
- Token required → user must send this token in each request (commonly in the Authorization header).
- Authorization check → system verifies whether the authenticated user is allowed to access that specific resource or action.
- If valid → grant access; else → return 401 Unauthorized or 403 Forbidden.
- Applied this to endpoints like /transactions to prevent anonymous or unauthorized access.

# Authentication vs Authorization
**Authentication = "Who are you?"**
Confirms the user’s identity (login with email/password).
Example: Showing your ID card at the entrance.

**Authorization = "What are you allowed to do?"**
Checks the user’s permissions after authentication.
Example: Having an entry pass that says you’re allowed to enter only the library but not the server room.

**In our app:**
***Authentication*** = user logs in and gets a token (like the ticket).
***Authorization*** = token is checked against rules (can this user access /transactions? which ones?).



