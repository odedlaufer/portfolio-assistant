from fastapi import FastAPI
from app.routers import analysis


app = FastAPI(title="Portfolio Analysis Assistant")

app.include_router(analysis.router)