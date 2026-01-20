from datetime import datetime, timedelta, timezone
from jose import jwt
from src.config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """创建访问令牌 (JWT)"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # 将过期时间放入 payload
    to_encode.update({"exp": expire})
    
    # 使用密钥签名
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
