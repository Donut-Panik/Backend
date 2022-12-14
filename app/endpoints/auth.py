from pydantic import Field
from datetime import timedelta

from fastapi import APIRouter, Depends, Form, status, Body, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.jwttoken import create_access_token
from app.db.connection import get_session
from app.utils.get_settings import auth
from app.utils.get_settings import get_settings
from app.schemas.auth import Token, RegUser, AuthUser, UserInfo, UserInfoAll
from app.queery.auth import check_nickname, create_user, find_by_nickname, get_info, get_info_public
from app.auth.oauth2 import get_current_user

registr_router = APIRouter(tags=["Authorization"])


@registr_router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(
    nickname: AuthUser = Body(...), session: AsyncSession = Depends(get_session)
) -> Token:
    await find_by_nickname(nickname.nickname, session)
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": nickname.nickname}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@registr_router.post(
    "/registration", response_model=Token, status_code=status.HTTP_200_OK
)
async def registration_user(
    new_user: RegUser = Body(...), session: AsyncSession = Depends(get_session)
) -> Token:
    await check_nickname(new_user.nickname, session)
    await create_user(new_user, session)
    # generate a jwt token and return
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.nickname}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@registr_router.get("/whoiam", response_model=UserInfo, status_code=status.HTTP_200_OK)
async def get_info_user(
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    return await get_info(current_user, session)


@registr_router.get("/info/{nickname}", response_model=UserInfoAll, status_code=status.HTTP_200_OK)
async def get_info_pub_user(nickname: str = Query(...),
                            session: AsyncSession = Depends(get_session),
                            current_user: str = Depends(get_current_user)):
    return await get_info_public(nickname, session)
