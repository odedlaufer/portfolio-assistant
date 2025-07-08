import matplotlib.pyplot as plt
import io
import pandas as pd


def plot_portfolio(df: pd.DataFrame) -> io.BytesIO:
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["TotalValue"])
    plt.title("Portfolio Value Over Time (6 Months)")
    plt.xlabel("Date")
    plt.ylabel("Value ($)")
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf
