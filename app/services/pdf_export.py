from fpdf import FPDF
from typing import Dict, Any
from app.utils.text import ascii_only


def generate_pdf(portfolio: Dict[str, Any]) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=ascii_only("Portfolio Analysis Report"), ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    total_value = portfolio["portfolio"]["total_value"]
    pdf.cell(200, 10, txt=f"Total Portfolio Value: ${total_value:,.2f}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Holdings:", ln=True)
    pdf.set_font("Arial", size=12)

    for stock in portfolio["portfolio"]["stocks"]:
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"{stock['symbol']} - {ascii_only(stock['company_name'])}", ln=True)
        pdf.cell(200, 10, txt=f"Sector: {ascii_only(stock['sector'])}", ln=True)
        pdf.cell(200, 10, txt=f"Current Price: ${stock['current_price']}", ln=True)
        pdf.cell(200, 10, txt=f"Total Value: ${stock['total_value']}", ln=True)
        pdf.multi_cell(0, 10, txt=ascii_only(stock["summary"]))

    # Recommendations
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt=ascii_only("Stock Recommendations (Same Sector)"), ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=12)

    for symbol, recs in portfolio["recommendations"].items():
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=f"Recommendations for {symbol}:", ln=True)
        pdf.set_font("Arial", size=12)
        for rec in recs:
            beta = rec.get("beta", "N/A")
            pdf.cell(200, 10, txt=f"{rec['symbol']} (Beta: {beta})", ln=True)
            pdf.multi_cell(0, 10, txt=ascii_only(rec["summary"]))
            pdf.ln(2)

    output = pdf.output(dest="S")
    if isinstance(output, str):
        return output.encode("latin-1")
    return output
