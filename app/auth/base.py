from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy import select
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.app_ctx import get_ctx_session
from app.data_layer.tables import User
from app.data_layer.schemas import UserDb

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


auth_scheme = HTTPBearer()


def create_access_token(email):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {'sub': email}

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDb:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    async with get_ctx_session() as session:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception

            query = await session.execute(select(User).where(User.email == email))
            user = query.fetchone()
            if user is None:
                raise credentials_exception

            user = user[0]
        except JWTError:
            raise credentials_exception

    return user
