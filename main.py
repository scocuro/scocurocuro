import csv
from datetime import date
from config import (
    UNDERLYING_TICKERS,
    STRIKE_PRICES,
    EARLY_REDEMPTION_BARRIERS,
    EARLY_REDEMPTION_COUPONS,
    EVALUATION_DATES,
    KNOCK_IN_BARRIERS,
    EMAIL_CONFIG,
)
from data_utils import fetch_last_close
from email_utils import send_email

def job():
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')

    headers = [
        "Ticker", "종가", "기준가격", "하락률", "Knock-in",
        "평가차수", "평가일", "Barrier", "Coupon"
    ]
    rows = []

    for ticker in UNDERLYING_TICKERS:
        strike      = STRIKE_PRICES[ticker]
        close_price = fetch_last_close(ticker)
        decline     = 1 - close_price / strike
        decline_txt = "해당없음" if decline < 0 else f"{decline*100:.2f}%"
        ki_price    = strike * KNOCK_IN_BARRIERS[ticker]

        # 다음 평가차수
        upcoming = next((i for i, d in EVALUATION_DATES[ticker].items() if d > today), None)
        if not upcoming:
            continue

        eval_date = EVALUATION_DATES[ticker][upcoming].strftime('%Y-%m-%d')
        barrier   = EARLY_REDEMPTION_BARRIERS[ticker][upcoming]
        coupon    = EARLY_REDEMPTION_COUPONS[ticker][upcoming]

        rows.append([
            ticker, close_price, strike, decline_txt,
            ki_price, upcoming, eval_date, barrier, coupon
        ])

    # CSV 생성
    output_file = 'els_report.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    # 이메일 전송
    send_email(
        subject=f"ELS Report ({today_str})",
        body="아래는 ELS 리포트 내용입니다:\n" +
             "\n".join([", ".join(map(str, row)) for row in rows]),
        attachments=[("els_report.csv", output_file)],
        config=EMAIL_CONFIG
    )

if __name__ == "__main__":
    job()
