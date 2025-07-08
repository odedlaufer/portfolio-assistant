import pandas as pd
from typing import List
from app.models import StockInput
from fastapi import UploadFile


async def parse_csv(file: UploadFile) -> List[StockInput]:
    df = pd.read_csv(file.file)
    portfolio = [
        StockInput(symbol=row["symbol"], quantity=int(row["quantity"]))
        for _, row in df.iterrows()
    ]
    return portfolio
