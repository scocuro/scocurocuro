import schedule, time
from datetime import datetime
from config import UNDERLYING_TICKERS, STRIKE_PRICES, EARLY_REDEMPTION_BARRIERS, EARLY_REDEMPTION_COUPONS, EMAIL_CONFIG
from data_utils import fetch_last_close, calc_decline_rate
from chart_utils import generate_price_chart
from email_utils import send_email

def job():
    today = datetime.now().strftime('%Y-%m-%d')
    body_lines = [f"ELS Daily Report — {today}\n"]
    attachments = []

    for ticker in UNDERLYING_TICKERS:
        strike = STRIKE_PRICES[ticker]
        close = fetch_last_close(ticker)
        decline = calc_decline_rate(close, strike)
        body_lines.append(
            f"{ticker}: 종가={close:.2f}, Strike={strike:.2f}, 하락률={decline:.2f}%"
        )

        chart_buf = generate_price_chart(ticker)
        attachments.append((f"{ticker}_chart_{today}.png", chart_buf))

        barriers = EARLY_REDEMPTION_BARRIERS[ticker]
        coupons = EARLY_REDEMPTION_COUPONS[ticker]
        for tranche in sorted(barriers):
            er_price = strike * (1 + coupons[tranche])
            barrier_pct = barriers[tranche] * 100
            body_lines.append(
                f"  → {tranche}차: Barrier ≥{barrier_pct:.1f}%, 상환가={er_price:.2f}"
            )

    body = '\n'.join(body_lines)
    send_email(
        subject=f"[{today}] ELS Daily Report",
        body=body,
        attachments=attachments,
        config=EMAIL_CONFIG
    )
    print(f"[{datetime.now()}] Email sent.")

schedule.every().day.at("09:00").do(job)

if __name__ == "__main__":
    job()
    # while True:
    #    schedule.run_pending()
    #    time.sleep(30)
