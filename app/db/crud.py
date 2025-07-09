from sqlalchemy.orm import Session

from app.db import models_db
from app.db.schemas import PortfolioCreate


def create_portfolio(db: Session, portfolio: PortfolioCreate):
    db_portfolio = models_db.Portfolio(name=portfolio.name)
    db.add(db_portfolio)
    db.flush()  # Ensures db_portfolio.id is populated before using it

    for stock in portfolio.stocks:
        db_stock = models_db.Stock(**stock.dict(), portfolio_id=db_portfolio.id)
        db.add(db_stock)

    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


def get_portfolio(db: Session, portfolio_id: int):
    return (
        db.query(models_db.Portfolio)
        .filter(models_db.Portfolio.id == portfolio_id)
        .first()
    )
