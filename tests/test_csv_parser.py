from io import BytesIO

import pytest
from fastapi import UploadFile

from app.utils.csv_parser import parse_csv


@pytest.mark.asyncio
async def test_parse_csv_valid():
    csv_content = "symbol,quantity\nAAPL,10\nMSFT,5"
    upload = UploadFile(filename="test.csv", file=BytesIO(csv_content.encode()))
    parsed = await parse_csv(upload)

    assert len(parsed) == 2
    assert parsed[0].symbol == "AAPL"
    assert parsed[0].quantity == 10


@pytest.mark.asyncio
async def test_prase_csv_invalid_format():
    bad_csv = "wrong,header\n123,456"
    upload = UploadFile(filename="bad.csv", file=BytesIO(bad_csv.encode()))

    with pytest.raises(Exception):
        await parse_csv(upload)
