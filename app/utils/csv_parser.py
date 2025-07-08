from typing import List

import pandas as pd
from fastapi import UploadFile

from app.models import StockInput


async def parse_csv(file: UploadFile) -> List[StockInput]:
    df = pd.read_csv(file.file)
    portfolio = [
        StockInput(symbol=row["symbol"], quantity=int(row["quantity"]))
        for _, row in df.iterrows()
    ]
    return portfolio
