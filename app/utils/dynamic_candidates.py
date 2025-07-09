import pandas as pd


def get_nasdaq_100_tickers() -> list[str]:
    try:
        url = "https://en.wikipedia.org/wiki/NASDAQ-100"
        tables = pd.read_html(url)
        tickers = tables[4]["Ticker"].tolist()
        return [ticker.replace(".", "-") for ticker in tickers]
    except Exception as e:
        print(f"Failed to fetch NASDAQ-100: {e}")
        return []
