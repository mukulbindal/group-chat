import jwt
from sqlalchemy.orm import Session
from .models import User
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "THIS IS MY SECRET KEY"


def generate_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')


def verify_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')


def authenticate(token, db: Session):
    user = verify_token(token)
    db_user = db.query(User).filter(User.id == user.id).first()
    if db_user is None:
        raise Exception('Authentication Error: No user')
    return db_user


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = verify_token(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
