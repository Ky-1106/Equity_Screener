import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import yfinance as yf

from backend import models, schemas, auth, stock_data
from backend.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Paisa Screener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/auth/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
        
    if not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
        
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/stocks/full")
def get_full_stocks(email: str = Depends(auth.get_current_user_email)):
    data = stock_data.fetch_full_stock_data()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch market data")
    return {"stocks": data}

@app.get("/api/stocks/live")
def get_live_prices(email: str = Depends(auth.get_current_user_email)):
    symbols = [s["t"] + ".NS" for s in stock_data.STATIC_STOCKS]
    try:
        tickers = yf.Tickers(" ".join(symbols))
        prices = {}
        for sym in symbols:
            try:
                info = tickers.tickers[sym].fast_info
                clean_sym = sym.replace(".NS", "")
                prices[clean_sym] = {
                    "price": info.last_price,
                    "change_pct": ((info.last_price - info.previous_close) / info.previous_close) * 100 if info.previous_close else 0
                }
            except Exception:
                pass
        return {"prices": prices}
    except Exception as e:
        print(f"Error fetching from yfinance: {e}")
    
    return {"prices": {}}

@app.get("/api/watchlist", response_model=List[schemas.WatchlistItemResponse])
def get_watchlist(email: str = Depends(auth.get_current_user_email), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.watchlist

@app.post("/api/watchlist", response_model=schemas.WatchlistItemResponse)
def add_to_watchlist(item: schemas.WatchlistItemCreate, email: str = Depends(auth.get_current_user_email), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Check if already in watchlist
    existing = db.query(models.WatchlistItem).filter(models.WatchlistItem.user_id == user.id, models.WatchlistItem.ticker == item.ticker).first()
    if existing:
        return existing
        
    new_item = models.WatchlistItem(user_id=user.id, ticker=item.ticker)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@app.delete("/api/watchlist/{ticker}")
def remove_from_watchlist(ticker: str, email: str = Depends(auth.get_current_user_email), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    item = db.query(models.WatchlistItem).filter(models.WatchlistItem.user_id == user.id, models.WatchlistItem.ticker == ticker).first()
    if item:
        db.delete(item)
        db.commit()
    return {"status": "success"}

@app.get("/api/users/me", response_model=schemas.UserOut)
def get_current_user_profile(email: str = Depends(auth.get_current_user_email), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users/me", response_model=schemas.UserOut)
def update_user_profile(profile: schemas.UserUpdateProfile, email: str = Depends(auth.get_current_user_email), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if profile.phone_number is not None:
        user.phone_number = profile.phone_number
    user.sms_alerts_enabled = profile.sms_alerts_enabled
    
    db.commit()
    db.refresh(user)
    return user

@app.put("/api/users/me/password")
def change_password(pw_data: schemas.UserUpdatePassword, email: str = Depends(auth.get_current_user_email), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if not auth.verify_password(pw_data.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
        
    user.hashed_password = auth.get_password_hash(pw_data.new_password)
    db.commit()
    return {"status": "success"}

# Serve Frontend Static Files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
