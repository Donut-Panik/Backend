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
from app.queery.categories import (
    add_category,
    delete_category,
    get_catgegories,
    put_category,
)

categories_router = APIRouter(tags=["Categories"])

responses = {
    status.HTTP_403_FORBIDDEN: {"detail": "Причина ошибки"},
    status.HTTP_400_BAD_REQUEST: {"detail": "Причина ошибки"},
}


@categories_router.post(
    "/magazine/category",
    response_model=CategoriesRequest,
    status_code=status.HTTP_201_CREATED,
    responses={**responses},
)
async def add_magazine_category(
    category: CategoriesRequest = Body(..., description="Category"),
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    # await check_admin(current_user, session)
    return await add_category(category, session)


@categories_router.get(
    "/magazine/categories",
    status_code=status.HTTP_200_OK,
    response_model=List[CategoriesResponse],
    responses={**responses},
)
async def get_magazine_categories(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
) -> List[CategoriesResponse]:
    #await check_admin(current_user, session)
    return await get_catgegories(session)


@categories_router.delete(
    "/magazine/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**responses},
)
async def delete_magazine_category(
    category_id: int = Path(..., description="Id categorie", ge=1),
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    # await check_admin(current_user, session)
    await delete_category(category_id, session)
    return SuccessfulResponse()


@categories_router.put(
    "/magazine/categories/{category_id}",
    response_model=SuccessfulResponse,
    status_code=status.HTTP_201_CREATED,
    responses={**responses},
)
async def put_magazine_category(
    category_id: int = Path(description="categorie_id", ge=1),
    new_categ: CategoriesRequestPut = Body(..., description="New name"),
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    # await check_admin(current_user, session)
    await put_category(
        category_id, session, new_categ.name,
    )
    return SuccessfulResponse()
