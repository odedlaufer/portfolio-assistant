from app.models import StockInput
from app.services.recommend import recommend_similar_stocks
from app.services.stock_data import get_stock_info


def export_analysis(portfolio: list[StockInput]) -> dict:
    results = [get_stock_info(stock) for stock in portfolio]
    total_value = sum(stock.total_value for stock in results)
    recommendations = recommend_similar_stocks(portfolio)

    return {
        "portfolio": {
            "total_value": total_value,
            "stocks": [stock.dict() for stock in results],
        },
        "recommendations": recommendations,
    }
