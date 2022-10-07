from datetime import timedelta

from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.jwttoken import create_access_token
from app.db.connection import get_session
from app.utils.get_settings import auth
from app.utils.get_settings import get_settings
from app.schemas.auth import Token, RegUser
from app.queery.auth import check_nickname, create_user, find_by_nickname
from app.auth.oauth2 import get_current_user
registr_router = APIRouter(tags=["Authorization"])


@registr_router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(nickname: str = Form(..., description="Никнейм", max_length=12),
                session: AsyncSession = Depends(get_session)) -> Token:
    await find_by_nickname(nickname, session)
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": nickname}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@registr_router.post('/registration',
                     response_model=Token,
                     status_code=status.HTTP_200_OK)
async def registration_user(new_user: RegUser,
                            session: AsyncSession = Depends(get_session)) -> Token:
    await check_nickname(new_user.nickname, session)
    await create_user(new_user, session)
    # generate a jwt token and return
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.nickname}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

