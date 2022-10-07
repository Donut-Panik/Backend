# pylint: skip-file
from typing import List, Optional

from pydantic import parse_obj_as
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import CategoriesModel, ProductCategoriesModel
from app.schemas.exceptions import BadRequest
from app.schemas.product import CategoriesRequest, CategoriesResponse


async def add_category(category: CategoriesRequest, session: AsyncSession):
    search_categor_query = select(CategoriesModel).where(
        and_(
            CategoriesModel.name == category.name,
        )
    )
    category_name = await session.scalar(search_categor_query)
    if category_name is not None:
        raise BadRequest("Категория существует")

    new_category = CategoriesModel(
        name=category.name,
    )
    session.add(new_category)
    await session.commit()
    return CategoriesRequest.from_orm(new_category)


async def get_catgegories(session: AsyncSession) -> List[CategoriesResponse]:
    query = (
        select(CategoriesModel)
        .filter(CategoriesModel.deleted == False)
    )
    items = await session.execute(query)
    return parse_obj_as(List[CategoriesResponse], items.scalars().unique().all())


async def delete_category(category_id: int, session: AsyncSession):
    delete_category_query = (
        update(CategoriesModel)
        .values(deleted=True)
        .where(
            and_(
                CategoriesModel.id == category_id,
            )
        )
    )
    # await session.execute(delete_prod_cat)
    await session.execute(delete_category_query)
    await session.commit()


async def put_category(
    category_id: int,
    session: AsyncSession,
    new_name: str,
) -> None:
    update_category_query = (
        update(CategoriesModel)
        .values(name=new_name)
        .where(
            and_(
                CategoriesModel.id == category_id,
            )
        )
    )
    await session.execute(update_category_query)
    await session.commit()


async def delete_product_ctegorie(
    categorie_id: Optional[int] = None, product_id: Optional[int] = None
):
    if categorie_id is None:
        query_del = delete(ProductCategoriesModel).where(
            ProductCategoriesModel.product_id == product_id
        )
    else:
        query_del = delete(ProductCategoriesModel).where(
            ProductCategoriesModel.category_id == categorie_id
        )
    return query_del
