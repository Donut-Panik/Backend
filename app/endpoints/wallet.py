from typing import List

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.schemas.auth import SuccessfulResponse

from app.auth.oauth2 import get_current_user
from app.schemas.wallet import History, Trade
from app.queery.wallet import get_history, remittance_to_user

wallet_router = APIRouter(tags=["Wallet"])


@wallet_router.post('/history',
                    status_code=status.HTTP_200_OK)
async def history_wallet(history: History = Body(...),
                         current_user: str = Depends(get_current_user),
                         session: AsyncSession = Depends(get_session)):
    return await get_history(history, current_user, session)


@wallet_router.post('/trade',
                    status_code=status.HTTP_200_OK)
async def remittance_wallet(trade: Trade = Body(...),
                            current_user: str = Depends(get_current_user),
                            session: AsyncSession = Depends(get_session)):
    return await remittance_to_user(trade, current_user, session)
