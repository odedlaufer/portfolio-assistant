from pydantic import BaseModel
from typing import List


class StockInput(BaseModel):
    symbol: str
    quantity: int


class StockAnalysis(BaseModel):
    symbol: str
    company_name: str
    sector: str
    current_price: float
    total_value: float
    summary: str


class PortfolioAnalysisResponse(BaseModel):
    total_portfolio_value: float
    stocks: List[StockAnalysis]