from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt

from app.core.config import settings

security = HTTPBearer()
public_key = settings.PUBLIC_AUTH_KEY

class TokenPayload(BaseModel):
    sub: str
    exp: int
    email: str | None = None

async def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenPayload:
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["ES256"],
            options={"verify_exp": True}
        )
        
        return TokenPayload(**payload)
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
