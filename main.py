from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
import jwt

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["users"]
users_collection = db["users"]

JWT_SECRET = "myjwtsecret"
JWT_ALGORITHM = "HS256"

security = HTTPBearer()

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UpdateUser(BaseModel):
    name: str = None
    email: EmailStr = None
    password: str = None
    role: str = None

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_token(user_id: str, user_role: str) -> str:
    payload = {"user_id": user_id, "user_role": user_role}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    decoded_token = verify_token(token)
    if decoded_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = users_collection.find_one({"_id": ObjectId(decoded_token["user_id"])})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = get_current_user(credentials)
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions")
    return user

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

@app.post("/users")
async def create_user(user: User):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = hash_password(user.password)
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role
    }
    result = users_collection.insert_one(user_data)
    user_id = str(result.inserted_id)
    token = create_token(user_id, user.role)
    return {"user_id": user_id, "access_token": token}

@app.post("/login")
async def login(login: Login):
    user = users_collection.find_one({"email": login.email})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(login.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return "mak"