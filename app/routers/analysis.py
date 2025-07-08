from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.models import PortfolioAnalysisResponse
from app.services.export import export_analysis
from app.services.performance import build_portfolio_value
from app.services.recommend import recommend_similar_stocks
from app.services.report_generator import generate_analysis_report
from app.services.stock_data import get_stock_info
from app.utils.csv_parser import parse_csv
from app.utils.error_handler import safe_call
from app.utils.plot import plot_portfolio

router = APIRouter()


@router.post("/analyze", response_model=PortfolioAnalysisResponse)
async def analyze_portfolio(file: UploadFile = File(...)):
    try:
        portfolio = await parse_csv(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing failed: {str(e)}")

    results = []
    for stock in portfolio:
        result = safe_call(
            lambda: get_stock_info(stock), context=f"get_stock_info: {stock.symbol}"
        )
        if result:
            results.append(result)

    if not results:
        raise HTTPException(
            status_code=400, detail="No valid stock data found in file."
        )

    total_value = sum(stock.total_value for stock in results)
    return PortfolioAnalysisResponse(total_portfolio_value=total_value, stocks=results)


@router.post("/performance-plot")
async def performance_plot(file: UploadFile = File(...)):
    try:
        portfolio = await parse_csv(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing failed: {str(e)}")

    values = safe_call(
        lambda: build_portfolio_value(portfolio), context="build_protfolio_value"
    )
    if values is None:
        raise HTTPException(status_code=500, detail="Failed to build portfolio values")

    img_buffer = safe_call(lambda: plot_portfolio(values), context="plot_portfolio")
    if img_buffer is None:
        raise HTTPException(status_code=500, detail="Failed to generate plot.")

    return StreamingResponse(img_buffer, media_type="image/png")


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


@router.post("/export/pdf", deprecated=True)
async def export_pdf(file: UploadFile = File(...)):
    raise HTTPException(
        status_code=410, detail="Endpoint is deprecated - use /generate-report"
    )


@router.post("/analyze-report")
async def anaylze_report(file: UploadFile = File(...)):
    pdf_bytes = await generate_analysis_report(file)
    return StreamingResponse(
        pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=portfolio_report.pdf"},
    )
