# pylint: disable=no-self-argument,too-few-public-methods
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, root_validator
from fastapi import Form


class ProductRequest(BaseModel):
    name: str = Form(..., description="Product Name", min_length=3, max_length=33,)
    descriotion: str = Form(..., description="Product описание",)
    price: float = Form(..., description="Product price", ge=1, lt=100000)
    category_id: int = Form(..., description="list categories", ge=1)


class ProductListGet(BaseModel):
    id: int
    name: str
    price: float
    category_id: int
    descriotion: str
    photo: str
    category_id: int
    category_name: str
    
    class Config:
        orm_mode = True


class CategoriesRequest(BaseModel):
    id: Optional[int] = Field(description="id category")
    name: str = Field(..., description="Категория блюда", max_length=30, min_length=3)

    @root_validator
    def check_name(cls, values):
        # new_name = values.get("name")
        # TODO вставить проверку на русские буквы
        return values

    class Config:
        orm_mode = True


class CategoriesResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CategoriesRequestPut(BaseModel):
    name: str = Field(..., description="Категория", min_length=3, max_length=33,)
