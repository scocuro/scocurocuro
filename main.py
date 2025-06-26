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
                b_txt = f"{barrier[0]*100:.1f}%/{barrier[1]*100:.1f}%"
                barrier_val = barrier
            else:
                b_txt = f"{barrier*100:.1f}%"
                barrier_val = barrier

            # 상환가 = Barrier 비율 * 기준가격
            if isinstance(barrier_val, (tuple, list)):
                # 리자드 차수 포함
                p_standard = barrier_val[0] * strike
                p_lookback = barrier_val[1] * strike
                redemption_txt = f"{p_standard:.2f}/{p_lookback:.2f}"
            else:
                redemption_txt = f"{barrier_val * strike:.2f}"

            tranche_txt = str(upcoming)
        else:
            # 만기 평가
            upcoming = '만기'
            eval_date = MATURITY_DATES[ticker].strftime('%Y-%m-%d')
            barrier_val = MATURITY_BARRIERS[ticker]
            b_txt = f"{barrier_val*100:.1f}%"
            # 상환가 계산: Barrier * 기준가격 or 기초자산 종가
            final_price = fetch_price_on_date(ticker, MATURITY_DATES[ticker])
            if final_price >= strike * barrier_val:
                redemption_txt = f"{(barrier_val * strike):.2f}"
            else:
                redemption_txt = f"{final_price:.2f}"
            tranche_txt = '만기'

        rows.append([
            ticker,
            f"{close_price:.2f}",
            f"{strike:.2f}",
            decline_txt,
            f"{ki_price:.2f}",
            tranche_txt,
            eval_date,
            b_txt,
            redemption_txt
        ])

    # 컬럼 너비 계산
    widths = [max(len(str(val)) for val in col) for col in zip(headers, *rows)]
    # 테이블 문자열 생성
    table_lines = []
    # 헤더
    header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep_line = "-|-".join('-' * widths[i] for i in range(len(headers)))
    table_lines.extend([header_line, sep_line])
    # 데이터 행
    for row in rows:
        line = " | ".join(str(val).ljust(widths[i]) for i, val in enumerate(row))
        table_lines.append(line)

    body = "\n".join(table_lines)

    # 이메일 전송
    send_email(
        subject=f"[{today_str}] ELS Daily Report",
        body=body,
        attachments=[(f"{t}_chart_{today_str}.png", generate_price_chart(t)) for t in UNDERLYING_TICKERS],
        config=EMAIL_CONFIG
    )

    print(f"[{datetime.now()}] Email sent.")

if __name__ == '__main__':
    job()
    # schedule.every().day.at("09:00").do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(30)
