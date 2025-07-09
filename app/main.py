import os
import sys

from fastapi import FastAPI

from app.routers import analysis, portfolio

print("Working directory:", os.getcwd())
print("sys.path:", sys.path)
app = FastAPI(title="Portfolio Analysis Assistant")

app.include_router(analysis.router)
app.include_router(portfolio.router)
