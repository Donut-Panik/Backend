# pylint: disable=W0613
from typing import List

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.schemas.auth import SuccessfulResponse
from app.schemas.product import (
    CategoriesRequest,
    CategoriesRequestPut,
    CategoriesResponse,
)
from app.auth.oauth2 import get_current_user


events_router = APIRouter(tags=["Events"])

