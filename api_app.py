from fastapi import FastAPI, HTTPException, Header, Depends
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# 1. Database Connection (Render will provide this via Environment Variables)
DATABASE_URL = os.getenv("DATABASE_URL") 
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

# 2. Function to check the database for the key
def verify_key(api_key: str):
    query = text("SELECT is_active, expiration_date FROM api_keys WHERE key_value = :key")
    with engine.connect() as conn:
        result = conn.execute(query, {"key": api_key}).fetchone()
        
    if not result:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    is_active, expiration_date = result
    
    if not is_active:
        raise HTTPException(status_code=403, detail="API Key is disabled")
        
    # Optional: Check if expired (PostgreSQL returns a date object)
    import datetime
    if expiration_date and expiration_date < datetime.date.today():
        raise HTTPException(status_code=403, detail="API Key has expired")
    
    return True

# 3. The "Product" Endpoint
@app.get("/multiply")
def multiply_by_100(number: float, x_api_key: str = Header(None)):
    # First, verify the user
    if verify_key(x_api_key):
        # If valid, perform the geophysics-grade math!
        result = number * 100
        return {"input": number, "result": result, "status": "success"}
