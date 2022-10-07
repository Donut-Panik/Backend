from sqlalchemy import select
from app.db.models import Users
from app.schemas.auth import RegUser
import httpx
from app.queery import baseUrl
from app.schemas.exceptions import UserFoundException, NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


new_wallet = '/v1/wallets/new'


async def check_nickname(nickname: str, session: AsyncSession):
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    if user:
        raise UserFoundException(error="Юзер с таким nickname существует")


async def create_user(new_user: RegUser, session: AsyncSession):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            baseUrl+new_wallet, timeout=10.0
        )
        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code, content=response.json()
            )
        resp = response.json()

    new_user = Users(nickname=new_user.nickname, name=new_user.name, surname=new_user.surname,
                     user_type="User", phone=new_user.phone,
                     wallet_private=resp["privateKey"], wallet_public=resp["publicKey"])
    session.add(new_user)
    await session.commit()


async def find_by_nickname(nickname: str, session: AsyncSession) -> str:
    user_query = select(Users).where(Users.phone == nickname)
    user: Users = await session.scalar(user_query)
    if not user:
        raise NotFoundException(error="Пользователь не найден")
