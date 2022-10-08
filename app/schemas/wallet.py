from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class History(BaseModel):
    page: int = Field(..., ge=1)
    offset: int = Field(..., ge=1)
    sort: str = Field(...,)
    publicKey: str = Field(...)


class TradeType(str, Enum):
    NFT = "NFT"
    RUBLE = "RUBLE"
    MATIC = "MATIC"


class Trade(BaseModel):
    type: TradeType
    fromPrivateKey: str
    toPublicKey: str
    amount: Optional[float]
    tokenId: Optional[int]
    