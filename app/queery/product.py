# pylint
from app.db.models import ProductsModel, ProductCategoriesModel, CategoriesModel
from sqlalchemy import select


async def create_product(name, descriotion, price, category_id, url, session):
    new_prodcut = ProductsModel(
        name=name, descriotion=descriotion, price=price, photo=url
    )
    session.add(new_prodcut)
    await session.flush()
    new_cat_pr = ProductCategoriesModel(
        product_id=new_prodcut.id, category_id=category_id
    )
    session.add(new_cat_pr)
    await session.commit()


async def get_products(categorie: str):
    query_join = (
        select(
            ProductsModel.id,
            ProductsModel.name,
            ProductsModel.photo,
            ProductsModel.descriotion,
            ProductsModel.price,
            CategoriesModel.id.label("category_id"),
            CategoriesModel.name.label("category_name"),
        )
        .join(
            ProductCategoriesModel,
            ProductCategoriesModel.product_id == ProductsModel.id,
        )
        .join(CategoriesModel, ProductCategoriesModel.category_id == CategoriesModel.id)
        .filter(ProductsModel.deleted == False)
    )
    if categorie is not None:
        query_join = query_join.filter(
            CategoriesModel.name.label("categorie_name") == categorie
        )
    return query_join
