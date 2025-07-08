import pytest

from app.models import StockInput
from app.services.stock_data import get_stock_info


def test_get_stock_info_valid():
    stock = StockInput(symbol="AAPL", quantity=10)
    info = get_stock_info(stock)

    assert info.symbol == "AAPL"
    assert info.total_value > 0
    assert info.company_name != "N/A"


def test_get_stock_info_invalid():
    stock = StockInput(symbol="FAKESTOCK1234", quantity=10)

    with pytest.raises(ValueError):
        get_stock_info(stock)
