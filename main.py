import schedule
import time
from datetime import date, datetime
from config import (
    UNDERLYING_TICKERS,
    STRIKE_PRICES,
    EARLY_REDEMPTION_BARRIERS,
    EARLY_REDEMPTION_COUPONS,
    EVALUATION_DATES,
    MATURITY_DATES,
    MATURITY_BARRIERS,
    MATURITY_COUPONS,
    KNOCK_IN_BARRIERS,
    EMAIL_CONFIG,
)
from data_utils import fetch_last_close, fetch_price_on_date
from chart_utils import generate_price_chart
from email_utils import send_email


def job():
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')

    # 결과 테이블 준비
    headers = [
        "Ticker", "종가", "기준가격", "하락률", "Knock-in", 
        "평가차수", "평가일", "Barrier", "상환가"
    ]
    rows = []

    for ticker in UNDERLYING_TICKERS:
        strike = STRIKE_PRICES[ticker]
        close_price = fetch_last_close(ticker)

        # 하락률 계산 (1 - 종가/기준가격)
        decline = 1 - close_price / strike
        decline_txt = "해당없음" if decline < 0 else f"{decline*100:.2f}%"

        # Knock-in 가격
        ki_price = strike * KNOCK_IN_BARRIERS[ticker]

        # 다음 평가차수 찾기
        eval_map = EVALUATION_DATES[ticker]
        tranches = sorted(eval_map.keys())
        upcoming = next((i for i in tranches if eval_map[i] > today), None)

        if upcoming:
            eval_date = eval_map[upcoming].strftime('%Y-%m-%d')
            barrier = EARLY_REDEMPTION_BARRIERS[ticker][upcoming]
            # Barrier 처리
            if isinstance(barrier, (tuple, list)):
                b_txt = f"{ba_
