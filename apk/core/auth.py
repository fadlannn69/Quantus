from fastapi import Security, HTTPException , Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlmodel import Session
from apk.database.session import get_session
from pathlib import Path
from dotenv import load_dotenv
import datetime
import jwt
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRIVATE_KEY_PATH = BASE_DIR / os.getenv("PRIVATE_KEY_PATH")
PUBLIC_KEY_PATH = BASE_DIR / os.getenv("PUBLIC_KEY_PATH")

with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "r") as f:
    PUBLIC_KEY = f.read()



class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['argon2'], deprecated="auto")
    secret = 'supersecret'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_id)
        }
        return jwt.encode(payload, PRIVATE_KEY, algorithm='ES256')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=['ES256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='TOKEN ANDA EXPIRED')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='TOKEN ANDA SALAH')
