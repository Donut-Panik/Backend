import httpx
from app.queery import baseUrl
from sqlalchemy import select
from app.schemas.wallet import History, Trade
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from app.db.models import Users


async def get_history(history: History, current_user: str, session: AsyncSession):
    user_query = select(Users).where(Users.nickname == current_user)
    user: Users = await session.scalar(user_query)
    new_wallet = f'/v1/wallets/{user.wallet_public}/history'
    async with httpx.AsyncClient() as client:
        response = await client.post(
            baseUrl+new_wallet, data={'page': history.page,
                                      'offset': history.offset,
                                      'sort': history.sort}, timeout=10.0
        )
        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code, content=response.json()
            )
    return JSONResponse(status_code=response.status_code, content=response.json())


async def remittance_to_user(trade: Trade, current_user: str, session: AsyncSession):
    match trade.type:
        case "NFT":
            new_wallet = '/v1/transfers/nft'
        case "RUBLE":
            new_wallet = '/v1/transfers/ruble'
        case "MATIC":
            new_wallet = '/v1/transfers/matic'
    # TODO: пофиксить amount
    async with httpx.AsyncClient() as client:
        response = await client.post(
            baseUrl+new_wallet, data={'fromPrivateKey': trade.fromPrivateKey,
                                      'toPublicKey': trade.toPublicKey,
                                      'amount': trade.amount}, timeout=10.0
        )
        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code, content=response.json()
            )
    return JSONResponse(status_code=response.status_code, content=response.json())
