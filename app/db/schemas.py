from datetime import datetime
from typing import List

from pydantic import BaseModel


class StockCreate(BaseModel):
    symbol: str
    company_name: str
    sector: str
    current_price: float
    total_value: float
    percentage_of_portfolio: float
    summary: str


class StockRead(StockCreate):
    id: int

    class Config:
        orm_mode = True


class PortfolioCreate(BaseModel):
    name: str
    stocks: List[StockCreate]


class PortfolioRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    stocks: List[StockRead]

    class Config:
        orm_mode = True
