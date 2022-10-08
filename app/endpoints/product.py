from typing import List, Optional

from fastapi import APIRouter, File, Query, UploadFile, status
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from app.auth.oauth2 import get_current_user
from app.schemas.product import ProductRequest, ProductListGet
from app.endpoints.download import downloadfilesproduct
from app.queery.product import create_product, get_products
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session
from app.schemas.auth import SuccessfulResponse


product_router = APIRouter(tags=["Product"])


@product_router.post('/product')
async def add_product(product: ProductRequest = Depends(),
                      upload_files: List[UploadFile] = File(...),
                      current_user: str = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)) -> JSONResponse:
    urls = await downloadfilesproduct(upload_files)
    await create_product(product, urls["photo1"], session)
    return SuccessfulResponse()


@product_router.get('/products',
                    response_model=Page[ProductListGet],
                    status_code=status.HTTP_200_OK,)
async def get_products_magazine(category: Optional[str] = Query(default=None, alias="category"),
                                current_user: str = Depends(get_current_user),
                                session: AsyncSession = Depends(get_session)):
    query_get_products = await get_products(category)
    return await paginate(session, query_get_products)
