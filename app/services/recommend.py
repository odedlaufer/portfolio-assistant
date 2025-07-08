import yfinance as yf
import pandas as pd
from app.models import StockInput
from typing import List

MAX_SUMMARY_LENGTH = 300


def trim_summary(text: str) -> str:
    if not text:
        return "No summary available."
    return text[:MAX_SUMMARY_LENGTH] + "..." if len(text) > MAX_SUMMARY_LENGTH else text


def recommend_similar_stocks(portfolio: List[StockInput], candidate_file: str = "data/candidate_stocks.csv"):
    candidates = pd.read_csv(candidate_file)["symbol"].tolist()
    recommendations = {}

    for stock in portfolio:
        try:
            stock_info = yf.Ticker(stock.symbol).info
            sector = stock_info.get("sector", None)
            beta = stock_info.get("beta", None)
        except Exception:
            continue

        if not sector or beta is None:
            continue

        similar = []
        for symbol in candidates:
            if symbol == stock.symbol:
                continue

            try:
                info = yf.Ticker(symbol).info
                if info.get("sector") == sector and info.get("beta") is not None:
                    similar.append({
                        "symbol": symbol,
                        "beta": info["beta"],
                        "summary": trim_summary(info.get("longBusinessSummary", ""))
                    })
            except Exception:
                continue

        similar_sorted = sorted(similar, key=lambda x: abs(x["beta"] - beta))
        recommendations[stock.symbol] = similar_sorted[:2]
   
    return recommendations
