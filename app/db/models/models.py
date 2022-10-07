# pylint: disable=R0903
from sqlalchemy import CheckConstraint, Column, ForeignKey, MetaData
from sqlalchemy.dialects.postgresql import (
    BOOLEAN,
    CHAR,
    INTEGER,
    JSONB,
    TIMESTAMP,
    VARCHAR,
    FLOAT
)
from sqlalchemy.orm import declarative_base
from enum import Enum
from app.db import convention

metadata = MetaData(naming_convention=convention)
DeclarativeBase = declarative_base(metadata=metadata)


class User_type(Enum):
    Admin = 1
    User = 2


class Users(DeclarativeBase):
    __tablename__ = "users"

    id = Column(
        "id", INTEGER, primary_key=True, unique=True, autoincrement=True, nullable=False
    )
    nickname = Column("nickname", VARCHAR(30), nullable=False)
    name = Column("name", VARCHAR(15), nullable=False)
    user_type = Column("user_type", VARCHAR(15), nullable=False)
    surname = Column("surname", VARCHAR(20), nullable=False)
    phone = Column("phone", CHAR(12), nullable=False)
    wallet_private = Column("wallet_private", VARCHAR(255), nullable=False)
    wallet_public = Column("wallet_public", VARCHAR(255), nullable=False)


class ProductsModel(DeclarativeBase):
    __tablename__ = "products"

    id = Column("id", INTEGER, primary_key=True, unique=True, autoincrement=True)
    name = Column("name", VARCHAR(255), nullable=False)
    deleted = Column("deleted", BOOLEAN, default=False)
    descriotion = Column("descriotion", VARCHAR(255), nullable=False)
    price = Column("price", FLOAT, nullable=False)
    photo = Column("photo", VARCHAR(255), nullable=False)
    __table_args__ = (CheckConstraint("price >= 0", name="check_price"),)


class CategoriesModel(DeclarativeBase):
    __tablename__ = "categories"

    id = Column("id", INTEGER, primary_key=True, unique=True, autoincrement=True)
    name = Column("name", VARCHAR(255), nullable=False)
    deleted = Column("deleted", BOOLEAN, default=False)


class ProductCategoriesModel(DeclarativeBase):
    __tablename__ = "product_categories"

    id = Column("id", INTEGER, primary_key=True, unique=True, autoincrement=True)
    product_id = Column(
        "product_id",
        INTEGER,
        ForeignKey(ProductsModel.id, ondelete="CASCADE"),
        nullable=False,
    )
    category_id = Column(
        "category_id",
        INTEGER,
        ForeignKey(CategoriesModel.id),
        nullable=False,
    )
