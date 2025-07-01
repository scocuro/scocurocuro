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

    rows = []
    for ticker in UNDERLYING_TICKERS:
        strike = STRIKE_PRICES[ticker]
        close_price = fetch_last_close(ticker)
        decline = 1 - close_price / strike
        decline_txt = "해당없음" if decline < 0 else f"{decline*100:.2f}%"
        ki_price = strike * KNOCK_IN_BARRIERS[ticker]

        # 다음 평가차수 찾기
        eval_map = EVALUATION_DATES[ticker]
        upcoming = next((i for i, d in eval_map.items() if d > today), None)
        if not upcoming:
            continue

        eval_date = eval_map[upcoming].strftime('%Y-%m-%d')
        barrier = EARLY_REDEMPTION_BARRIERS[ticker][upcoming]
        coupon = EARLY_REDEMPTION_COUPONS[ticker][upcoming]

        rows.append([
            ticker, close_price, strike, decline_txt,
            ki_price, upcoming, eval_date, barrier, coupon
        ])

    # 이메일 발송
    send_email(
        subject=f"ELS Report ({today_str})",
        body="아래는 ELS 리포트 내용입니다:\n" +
             "\n".join([", ".join(map(str, row)) for row in rows]),
        attachments=[("els_report.csv", "path_to_your_report.csv")],
        config=EMAIL_CONFIG
    )

if __name__ == "__main__":
    job()
