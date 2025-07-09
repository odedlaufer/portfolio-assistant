from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import crud, models_db
from app.db.database import engine, get_db
from app.db.schemas import PortfolioCreate, PortfolioRead

models_db.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/save-portfolio", response_model=PortfolioRead)
def save_portfolio(portfolio: PortfolioCreate, db: Session = Depends(get_db)):
    return crud.create_portfolio(db, portfolio)


@router.get("/portfolio/{portfolio_id}", response_model=PortfolioRead)
def read_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    return crud.get_portfolio(db, portfolio_id)
