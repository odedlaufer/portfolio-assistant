import io
from typing import List

from fastapi import HTTPException, UploadFile

from app.models import StockInput
from app.services.pdf_export import generate_pdf
from app.services.recommend import recommend_for_stock
from app.services.stock_data import get_stock_info
from app.utils.csv_parser import parse_csv
from app.utils.error_handler import safe_call


async def generate_analysis_report(file: UploadFile) -> io.BytesIO:
    try:
        portfolio_input: List[StockInput] = await parse_csv(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing failed: {str(e)}")

    stocks = []
    for stock in portfolio_input:
        enriched = safe_call(
            lambda: get_stock_info(stock), context=f"get_stock_info: {stock.symbol}"
        )
        if enriched:
            stocks.append(enriched)

    if not stocks:
        raise HTTPException(status_code=400, detail="No valid stocks found.")

    total_value = sum(s.total_value for s in stocks)

    rec_map = {}
    for stock in stocks:
        symbol = stock.symbol
        recs = safe_call(
            lambda s=symbol: recommend_for_stock(s), context=f"recommend: {symbol}"
        )
        if recs:
            rec_map[symbol] = recs

    pdf_data = {
        "portfolio": {"total_value": total_value, "stocks": [s.dict() for s in stocks]},
        "recommendations": rec_map,
    }

    return io.BytesIO(generate_pdf(pdf_data))
