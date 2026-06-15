from fastapi import FastAPI, HTTPException 
from fastapi import File , UploadFile
from pydantic import BaseModel

from passlib.context import CryptContext
from jose import jwt

from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import os

# ---------------- APP ----------------
app = FastAPI()

# ---------------- DATABASE URL ----------------
DATABASE_URL = "sqlite:///./users.db"

# ---------------- DATABASE SETUP ----------------
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ---------------- USER TABLE ----------------
class UserTable(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True
    )

    password = Column(String)

# ---------------- CREATE TABLE ----------------
Base.metadata.create_all(bind=engine)

# ---------------- JWT ----------------
SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

# ---------------- PASSWORD HASH ----------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ---------------- USER MODEL ----------------
class User(BaseModel):

    username: str

    password: str
    
# ---------------- FORGOT PASSWORD MODEL ----------------
class ForgotPassword(BaseModel):

    username: str
    new_password: str

# ---------------- HASH PASSWORD ----------------
def hash_password(password):

    return pwd_context.hash(password)

# ---------------- VERIFY PASSWORD ----------------
def verify_password(plain, hashed):

    return pwd_context.verify(
        plain,
        hashed
    )

# ---------------- CREATE TOKEN ----------------
def create_token(data):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# ---------------- SIGNUP ----------------
@app.post("/signup")
def signup(user: User):

    db = SessionLocal()

    existing_user = db.query(UserTable).filter(
        UserTable.username == user.username
    ).first()

    if existing_user:

        db.close()

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_pw = hash_password(
        user.password
    )

    new_user = UserTable(
        username=user.username,
        password=hashed_pw
    )

    db.add(new_user)

    db.commit()

    db.close()

    return {
        "message": "Signup successful"
    }

# ---------------- LOGIN ----------------
@app.post("/login")
def login(user: User):

    db = SessionLocal()

    db_user = db.query(UserTable).filter(
        UserTable.username == user.username
    ).first()

    db.close()

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_token({
        "sub": user.username
    })

    return {
        "token": token,
        "message": "Login successful"
    }
    @app.post("/forgot-password")
    def forgot_password(data: ForgotPassword):

      db = SessionLocal()

    user = db.query(UserTable).filter(
        UserTable.username == data.username
    ).first()

    if not user:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.password = hash_password(
        data.new_password
    )

    db.commit()

    db.close()

    return {
        "message": "Password reset successful"
    }
# ---------------- ANALYZE ----------------
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    try:
        content = await file.read()

        # FILE HANDLING
        if file.filename.endswith(".csv"):

            df = pd.read_csv(
                io.StringIO(content.decode("utf-8"))
            )

        elif file.filename.endswith((".xlsx", ".xls")):

            df = pd.read_excel(
                io.BytesIO(content)
            )

        elif file.filename.endswith(".json"):

            df = pd.read_json(
                io.StringIO(content.decode("utf-8"))
            )

        else:
            return {
                "error": "Unsupported file"
            }

        # CLEAN
        df.columns = df.columns.str.strip().str.lower()

        df = df.fillna(0)

        # AUTO COLUMNS
        if "quantity" not in df.columns:
            df["quantity"] = 1

        if "sales" not in df.columns:
            df["sales"] = df["quantity"] * 100

        if "profit" not in df.columns:
            df["profit"] = df["sales"] * 0.3

        if "discount" not in df.columns:
            df["discount"] = 0.05

        if "shipping_cost" not in df.columns:
            df["shipping_cost"] = df["sales"] * 0.05

        # DATE
        if "order_date" not in df.columns:
            df["order_date"] = pd.Timestamp.today()

        df["order_date"] = pd.to_datetime(
            df["order_date"]
        )

        # CATEGORY
        if "category" not in df.columns:
            df["category"] = "General"

        # VENDOR ID
        if "vendor id" not in df.columns:

            df["vendor id"] = [
                "V" + str(i + 1).zfill(3)
                for i in range(len(df))
            ]

        # RISK LOGIC
        df["risk_status"] = (
            (df["profit"] < 100) |
            (df["discount"] > 0.2) |
            (df["sales"] < 500)
        ).astype(int)

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        return {
            "error": str(e)
        }
