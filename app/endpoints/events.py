# pylint: disable=W0613
from typing import List,Optional
from datetime import date
from fastapi import APIRouter, Body, Depends, Path, status, Form, File, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.db.connection import get_session
from app.schemas.auth import SuccessfulResponse
from app.schemas.events import EventAdd, ListEventOut,ListMyEventOut
from app.auth.oauth2 import get_current_user
from app.schemas.wallet import TradeType
from app.endpoints.download import downloadfilesproduct
from app.queery.events import create_events, get_events, complete_event, accept_event, get_myevents
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate


events_router = APIRouter(tags=["Events"])


@events_router.post('/event',
                    status_code=status.HTTP_200_OK,)
async def add_new_event(
    name: str = Form(
        ...,
        description="Events name",
        min_length=3,
        max_length=33,
    ),
    descriotion: str = Form(
        ...,
        description="Event описание",
    ),
    price: float = Form(..., description="Event награда", lt=100000),
    type: TradeType = Form(..., description="Type награды"),
    date_end: date = Form(..., description="Date end"),
    upload_files: List[UploadFile] = File(...),
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    urls = await downloadfilesproduct(upload_files)
    await create_events(name, date_end, descriotion, price, type, urls["photo1"], session, current_user)
    return SuccessfulResponse()


@events_router.get(
    "/events",
    response_model=Page[ListEventOut],
    status_code=status.HTTP_200_OK,
)
async def get_events_user(
    category: Optional[str] = Query(default=None, alias="category"),
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    query_get_products = await get_events(category)
    return await paginate(session, query_get_products)


@events_router.post(
    '/accept/{event_id}',
    status_code=status.HTTP_200_OK
)
async def accept_event_user(event_id: int = Path(...),
                            current_user: str = Depends(get_current_user),
                            session: AsyncSession = Depends(get_session)):
    await accept_event(event_id, current_user, session)
    return SuccessfulResponse()


@events_router.post(
    '/complete/{event_id}',
    status_code=status.HTTP_200_OK
)
async def complete_event_user(event_id: int = Path(...),
                              current_user: str = Depends(get_current_user),
                              session: AsyncSession = Depends(get_session)):
    return await complete_event(event_id, session, current_user)


@events_router.get(
    "/myevents",
    response_model=Page[ListMyEventOut],
    status_code=status.HTTP_200_OK,
)
async def get_events_myuser(
    category: Optional[str] = Query(default=None, alias="category"),
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    query_get_products = await get_myevents(category, current_user, session)
    return await paginate(session, query_get_products)