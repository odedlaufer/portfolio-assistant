import yfinance as yf

from app.models import StockAnalysis, StockInput


def get_stock_info(stock: StockInput) -> StockAnalysis:
    ticker = yf.Ticker(stock.symbol)
    info = ticker.info

    current_price = info.get("currentPrice")
    company_name = info.get("shortName")

    if current_price is None or company_name is None:
        raise ValueError(f"Invalid stock data for symbol: {stock.symbol}")

    sector = info.get("sector", "N/A")
    full_summary = info.get("longBusinessSummary", "N/A")
    summary = full_summary[:300] + "..." if len(full_summary) > 300 else full_summary
    total_value = current_price * stock.quantity

    return StockAnalysis(
        symbol=stock.symbol,
        company_name=company_name,
        sector=sector,
        current_price=current_price,
        total_value=total_value,
        summary=summary,
    )
