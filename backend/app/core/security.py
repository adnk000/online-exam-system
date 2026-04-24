import os
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)



SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Use a stable Fernet key so encrypted answers remain decryptable after app restart.
SECRET_ENCRYPTION_KEY = os.environ.get(
    "SECRET_ENCRYPTION_KEY",
    "h9mfjDMaSgLFkCwqHVtZ-yWeDQuMrBA3vAqQUIplGZ4="
)
cipher = Fernet(SECRET_ENCRYPTION_KEY.encode() if isinstance(SECRET_ENCRYPTION_KEY, str) else SECRET_ENCRYPTION_KEY)

def encrypt_answer(answer: str):
    return cipher.encrypt(answer.encode()).decode()

def decrypt_answer(encrypted: str):
    return cipher.decrypt(encrypted.encode()).decode()

