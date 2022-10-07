import json
from typing import List

from fastapi import APIRouter, File, Form, Query, UploadFile, status
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from fastapi_pagination import Page
from app.auth.oauth2 import get_current_user
from app.schemas.product import ProductRequest
from app.endpoints.download import downloadfilesproduct
product_router = APIRouter(tags=["Product"])


@product_router.post('/product')
async def add_product(product: ProductRequest,
                      upload_files: List[UploadFile] = File(...),
                      current_user: str = Depends(get_current_user)) -> JSONResponse:
    urls = await downloadfilesproduct(upload_files)
