from fastapi import FastAPI, HTTPException UploadFile,File
from pydantic import BaseModel
import sqlite3
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# -------------------- CONFIG --------------------
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

DB = "users.db"

# -------------------- MODEL --------------------
class User(BaseModel):
    username: str
    password: str

# -------------------- DB SETUP --------------------
def create_table():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

create_table()

# -------------------- HASH FUNCTIONS --------------------
def hash_password(password):
    return pwd_context.hash(password[:72])

def verify_password(plain, hashed):
    plain = plain[:72]
    return pwd_context.verify(plain, hashed)

# -------------------- TOKEN --------------------
def create_token(data):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -------------------- SIGNUP --------------------
@app.post("/signup")
def signup(user: User):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    hashed_pw = hash_password(user.password)

    try:
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, hashed_pw)
        )
        conn.commit()
        return {"message": "Signup successful"}

    except:
        return {"error": "User already exists"}

    finally:
        conn.close()

# -------------------- LOGIN --------------------
@app.post("/login")
def login(user: User):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "SELECT username, password FROM users WHERE username=?",
        (user.username,)
    )

    result = c.fetchone()
    conn.close()

    print("USER INPUT:", user.username, user.password)
    print("DB RESULT:", result)

    if result:
        stored_password = result[1]
        print("STORED HASH:", stored_password)

        if verify_password(user.password, stored_password):
            print("PASSWORD MATCH ✅")

            token = create_token({"sub": user.username})
            return {"token": token}

        else:
            print("PASSWORD MISMATCH ❌")
            raise HTTPException(status_code=401, detail="Invalid credentials")

    else:
        print("USER NOT FOUND ❌")
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        content = await file.read()

        # FILE HANDLING
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        elif file.filename.endswith((".xlsx",".xls")):
            df = pd.read_excel(io.BytesIO(content))
        elif file.filename.endswith(".json"):
            df = pd.read_json(io.StringIO(content.decode("utf-8")))
        else:
            return {"error": "Unsupported file"}

        # CLEAN
        df.columns = df.columns.str.strip().str.lower()
        df = df.fillna(0)

        # AUTO COLUMN CREATION
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

        df["order_date"] = pd.to_datetime(df["order_date"])

        # CATEGORY
        if "category" not in df.columns:
            df["category"] = "General"

        if "vendor id" not in df.columns:
            df["vendor id"] = ["V"+str(i+1).zfill(3) for i in range(len(df))]

        # RISK LOGIC
        df["risk_status"] = (
            (df["profit"] < 100) |
            (df["discount"] > 0.2) |
            (df["sales"] < 500)
        ).astype(int)

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
