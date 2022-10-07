# pylint: disable=no-self-argument,too-few-public-methods
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, root_validator


class ProductRequest(BaseModel):
    id: Optional[int] = Field(description="id response")
    name: str = Field(..., description="Product Name", min_length=3, max_length=33,
                      regex="^[а-яА-Я ]{3,33}$")
    descriotion: str = Field(..., description="Product описание",)
    price: float = Field(..., description="Product price", ge=1, lt=100000)
    category_id: int = Field(..., description="list categories", ge=1)
