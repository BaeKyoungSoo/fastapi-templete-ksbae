import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Request
from passlib.context import CryptContext
from app.api.models import User  # 예시: 실제 User 모델을 import

# 이 부분은 환경에 따라 조정되어야 합니다.
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 패스워드를 해싱하는 데 사용할 암호화 컨텍스트 생성
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 사용자 인증 로직: 예시를 위한 간단한 함수입니다.
def authenticate_user(username: str, password: str) -> Optional[User]:
    # user = get_user_by_username(username)
    user = username
    if user and verify_password(password, user.hashed_password):
        return user
    return None

# 패스워드 검증
def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

# 토큰 생성
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # 기본 만료 시간
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 토큰 디코딩
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 토큰 추출 로직: 예시를 위한 간단한 함수입니다.
def get_token_from_request(request: Request) -> Optional[str]:
    authorization_header = request.headers.get("Authorization")
    if authorization_header and authorization_header.startswith("Bearer "):
        token = authorization_header.split(" ")[1]
        return token
    return None
