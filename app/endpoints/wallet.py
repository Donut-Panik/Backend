from typing import List
import uuid
from fastapi import APIRouter, Body, Depends, Path, status, UploadFile, File, Form,Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.schemas.auth import SuccessfulResponse

from app.auth.oauth2 import get_current_user
from app.schemas.wallet import History, Trade, NftGen, transactionHash
from app.queery.wallet import get_history, remittance_to_user, create_nft, check_tran
from app.endpoints.s3 import go

wallet_router = APIRouter(tags=["Wallet"])


@wallet_router.post("/history", status_code=status.HTTP_200_OK)
async def history_wallet(
    history: History = Body(...),
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await get_history(history, current_user, session)


@wallet_router.post("/trade", status_code=status.HTTP_200_OK)
async def remittance_wallet(
    trade: Trade = Body(...),
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await remittance_to_user(trade, current_user, session)


@wallet_router.post(
    "/generate/nft", response_model=transactionHash, status_code=status.HTTP_200_OK
)
async def generate_nft(
    nftCount: int = Form(..., description="list categories", ge=1),
    file: UploadFile = File(description="A file read as UploadFile"),
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    key = await go(str(uuid.uuid4()) + "/" + file.filename, file.file)
    return await create_nft(key, current_user, session, nftCount)


@wallet_router.get('/status/{transactionHash}')
async def get_status(transactionHash: str = Query(...),
                     current_user: str = Depends(get_current_user)):
    return await check_tran(transactionHash)
