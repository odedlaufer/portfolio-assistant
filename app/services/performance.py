import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from app.models import StockInput
from typing import List


def fetch_historical_values(stock: StockInput, start_date, end_date) -> pd.DataFrame:
    ticker = yf.Ticker(stock.symbol)
    hist = ticker.history(start=start_date, end=end_date)

    if hist.empty:
        return pd.DataFrame()

    hist["HoldingValue"] = hist["Close"] * stock.quantity
    df = hist[["HoldingValue"]].rename(columns={"HoldingValue": stock.symbol})
    return df


def build_portfolio_value(portfolio: List[StockInput], days_back=180) -> pd.DataFrame:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days_back)

    total_df = pd.DataFrame()

    for stock in portfolio:
        stock_df = fetch_historical_values(stock, start_date, end_date)
        if stock_df.empty:
            continue

        if total_df.empty:
            total_df = stock_df
        else:
            total_df = total_df.join(stock_df, how="outer")
    
    total_df.fillna(0, inplace=True)
    total_df["TotalValue"] = total_df.sum(axis=1)
    return total_df