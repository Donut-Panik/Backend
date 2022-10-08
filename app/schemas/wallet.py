from tkinter.messagebox import YES
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class History(BaseModel):
    page: int = Field(..., ge=1)
    offset: int = Field(..., ge=1)
    sort: str = Field(
        ...,
    )


class TradeType(str, Enum):
    NFT = "NFT"
    RUBLE = "RUBLE"
    MATIC = "MATIC"


class NftType(str, Enum):
    YES = "YES"
    NO = "NO"


class Trade(BaseModel):
    type: TradeType
    fromPrivateKey: str
    toPublicKey: str
    amount: Optional[float]
    tokenId: Optional[int]


class NftGen(BaseModel):
    uri: str = Field(...)
    nftCount: int = Field(ge=1, lt=20)
    photo: NftType


class transactionHash(BaseModel):
    transactionHash: str
