# FastAPI Finance Tracker

A backend API built with **FastAPI** and **SQLAlchemy ORM** to track personal finance.  
Currently supports **CRUD** operations for transactions, **JWT-based authentication**, password hashing using **bcrypt** algorithm and **access-protected endpoints**.

---

## ✨ Features (current progress)

- ✅ **Users ↔ Transactions** relationship (one-to-many via `transactions.user_id` FK)
- ✅ **CRUD** for transactions
  - `POST /transactions` → create a transaction
  - `GET /transactions` → list transactions (with pagination + filtering)
  - `GET /transactions/{id}` → fetch a single transaction
  - `PUT /transactions/{id}` → update a transaction
  - `DELETE /transactions/{id}` → delete a transaction
- ✅ **Pagination, filtering, and sorting** for listing transactions  
  - `?skip=0&limit=20` → pagination  
  - `?from=YYYY-MM-DD&to=YYYY-MM-DD` → filter by date range  
  - `?type=income|expense` → filter by transaction type  
  - `?min_amount=&max_amount=` → filter by amount range  
  - `?order_by=created_at&direction=desc` → sorting
- ✅ **Validation** with Pydantic schemas
- ✅ **Password hashing (bcrypt)**  
  - Passwords are **never stored in plain text**.  
  - On signup, passwords are **hashed with bcrypt**; on login, we **verify via hash comparison**.
- ✅ **JWT Authentication** (`/auth/signup`, `/auth/login`)
- ✅ **Access-protected endpoints** (require `Authorization: Bearer <token>`)
- ✅ **Per-user transactions** (multi-user support) 

---

## 📂 Project Structure

```
fastapi-finance-tracker/
├── db.py          # Database setup (engine, session, Base)
├── models.py      # SQLAlchemy models (Transaction)
├── schemas.py     # Pydantic schemas for request/response
├── main.py        # FastAPI app + endpoints
├── notes.md       # Personal learning notes
├── .gitignore     # Ignore venv, db, cache files
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/sahil-katle/fastapi-finance-tracker.git
cd fastapi-finance-tracker
```

### 2. Create a virtual environment & install deps
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic
```

### 3. Run the app
```bash
uvicorn main:app --reload
```

Now open: 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Example Request (POST /transactions)

```json
{
  "description": "Coffee",
  "amount": 3.5,
  "kind": "expense",
  "category": "food",
  "occurred_on": "2025-08-31",
  "note": "Latte from Starbucks"
}
```

---

## 📌 Roadmap
- [ ] Monthly & category-based reports  
- [ ] Budget alerts (80/90/100%)  
- [ ] CSV/Excel export  
- [ ] Deployment with Docker  
- [ ] AI integration (natural language queries & auto-categorization)  

---

## 🛠 Tech Stack

- **FastAPI** – high-performance Python web framework  
- **SQLAlchemy** – ORM for database  
- **Pydantic** – data validation  
- **SQLite** – lightweight local database  
- **Uvicorn** – ASGI server  

---

👤 **Author**: [@sahil-katle](https://github.com/sahil-katle)
