# pylint: disable=no-self-argument,too-few-public-methods
from typing import Optional
from pydantic import BaseModel, Field, root_validator
from fastapi import Form
from app.schemas.wallet import TradeType


class EventAdd(BaseModel):
    name: str = Field(...)
    descriotion: str = Field(...)
    price: float = Field(...)
    type: TradeType = Field(...)


class ListEventOut(BaseModel):
    id : int
    name: str
    descriotion: str
    price: float
    type: TradeType


class AcceptEvent(BaseModel):
    pass