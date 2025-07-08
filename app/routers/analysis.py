from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import StreamingResponse
from app.models import PortfolioAnalysisResponse
from app.services.performance import build_portfolio_value
from app.services.recommend import recommend_similar_stocks
from app.services.stock_data import get_stock_info
from app.services.export import export_analysis
from app.services.pdf_export import generate_pdf
from app.utils.csv_parser import parse_csv
from app.utils.plot import plot_portfolio
import io

router = APIRouter()


@router.post("/analyze", response_model=PortfolioAnalysisResponse)
async def analyze_portfolio(file: UploadFile = File(...)):
    portfolio = await parse_csv(file)

    results = [get_stock_info(stock) for stock in portfolio]
    total_value = sum(stock.total_value for stock in results)

    return PortfolioAnalysisResponse(total_portfolio_value=total_value, stocks=results)


@router.post("/performance-plot")
async def performance_plot(file: UploadFile = File(...)):
    portfolio = await parse_csv(file)
    df = build_portfolio_value(portfolio)
    plot_buf = plot_portfolio(df)
    return StreamingResponse(plot_buf, media_type="image/png")


@router.post("/recommend")
async def recommend(file: UploadFile = File(...)):
    portfolio = await parse_csv(file)
    recs = recommend_similar_stocks(portfolio)
    return recs


@router.post("/export")
async def export(file: UploadFile = File(...)):
    portfolio = await parse_csv(file)
    result = export_analysis(portfolio)
    return result


@router.post("/export/pdf")
async def export_pdf(file: UploadFile = File(...)):
    portfolio = await parse_csv(file)
    analysis = export_analysis(portfolio)
    pdf_bytes = generate_pdf(analysis)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf")