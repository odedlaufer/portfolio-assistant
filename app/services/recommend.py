from typing import Dict, List

import yfinance as yf

from app.models import StockInput
from app.utils.dynamic_candidates import get_nasdaq_100_tickers

MAX_SUMMARY_LENGTH = 300


def trim_summary(text: str) -> str:
    if not text:
        return "No summary available."
    return text[:MAX_SUMMARY_LENGTH] + "..." if len(text) > MAX_SUMMARY_LENGTH else text


def recommend_for_stock(symbol: str, candidates: List[str]) -> List[dict]:
    try:
        stock_info = yf.Ticker(symbol).info
        sector = stock_info.get("sector", None)
        beta = stock_info.get("beta", None)
    except Exception:
        return []

    if not sector or beta is None:
        return []

    similar = []
    for candidate in candidates:
        if candidate == symbol:
            continue
        try:
            info = yf.Ticker(candidate).info
            if info.get("sector") == sector and info.get("beta") is not None:
                similar.append(
                    {
                        "symbol": candidate,
                        "beta": info["beta"],
                        "summary": trim_summary(info.get("longBusinessSummary", "")),
                    }
                )
        except Exception:
            continue

    similar_sorted = sorted(similar, key=lambda x: abs(x["beta"] - beta))
    return similar_sorted[:2]


def recommend_similar_stocks(portfolio: List[StockInput]) -> Dict[str, List[dict]]:
    candidates = get_nasdaq_100_tickers()
    print(f"Candidate tickers fetched: {len(candidates)} → {candidates[:5]}")
    return {
        stock.symbol: recommend_for_stock(stock.symbol, candidates)
        for stock in portfolio
    }


# def recommend_similar_stocks(
#    portfolio: List[StockInput], candidate_file: str = "data/candidate_stocks.csv"
# ) -> Dict[str, List[dict]]:
#    return {
#        stock.symbol: recommend_for_stock(stock.symbol, candidate_file)
#        for stock in portfolio
#    }
