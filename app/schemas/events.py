# pylint: disable=no-self-argument,too-few-public-methods
from typing import Optional
from pydantic import BaseModel, Field, root_validator
from fastapi import Form
from app.schemas.wallet import TradeType
from datetime import date


class EventAdd(BaseModel):
    name: str = Field(...)
    descriotion: str = Field(...)
    price: float = Field(...)
    type: TradeType = Field(...)


class ListEventOut(BaseModel):
    id: int
    name: str
    descriotion: str
    price: float
    photo: str
    type: TradeType
    nickname: str
    user_name: str
    user_surname: str
    date_end: date


class ListMyEventOut(BaseModel):
    id: int
    name: str
    descriotion: str
    price: float
    photo: str
    type: TradeType
    nickname: str
    user_name: str
    user_surname: str
    date_end: date
    condition: str


class AcceptEvent(BaseModel):
    pass