import schedule
import time
from datetime import date, datetime, timedelta
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

    body_lines = [f"ELS Daily Report — {today_str}\n"]
    attachments = []

    for ticker in UNDERLYING_TICKERS:
        strike = STRIKE_PRICES[ticker]
        close_price = fetch_last_close(ticker)

        # 하락률 계산 (1 - 종가/기준가격)
        decline = 1 - close_price / strike
        decline_txt = "해당없음" if decline < 0 else f"{decline*100:.2f}%"

        # Knock-in 가격
        ki_price = strike * KNOCK_IN_BARRIERS[ticker]

        body_lines.append(
            f"{ticker}: 종가={close_price:.2f}, 기준가격={strike:.2f}, "
            f"하락률={decline_txt}, Knock-in 가격={ki_price:.2f}"
        )

        # 오늘 이후 첫 조기상환 평가차수
        eval_map = EVALUATION_DATES[ticker]
        upcoming = next(
            (i for i, d in sorted(eval_map.items()) if d > today),
            None
        )

        if upcoming:
            eval_date = eval_map[upcoming].strftime('%Y-%m-%d')
            barrier = EARLY_REDEMPTION_BARRIERS[ticker][upcoming]
            # Barrier tuple 처리 (3차 리자드)
            if isinstance(barrier, (tuple, list)):
                b_std, b_lb = barrier
                barrier_txt = (
                    f"Barrier≥{b_std*100:.1f}% / Look-back≥{b_lb*100:.1f}%"
                )
            else:
                barrier_txt = f"Barrier≥{barrier*100:.1f}%"

            coupon = EARLY_REDEMPTION_COUPONS[ticker][upcoming]
            # Coupon tuple 처리 (3차 리자드)
            if isinstance(coupon, (tuple, list)):
                p1 = strike * (1 + coupon[0])
                p2 = strike * (1 + coupon[1])
                redemption_txt = f"상환가={p1:.2f} / 리자드={p2:.2f}"
            else:
                redemption_txt = f"상환가={strike*(1 + coupon):.2f}"

            body_lines.append(
                f"  → {upcoming}차 평가일: {eval_date}, {barrier_txt}, {redemption_txt}"
            )
        else:
            # 모든 조기상환 일정 경과 시 만기 평가
            maturity_date = MATURITY_DATES[ticker].strftime('%Y-%m-%d')
            m_barrier = MATURITY_BARRIERS[ticker]
            m_coupon = MATURITY_COUPONS[ticker]
            # 만기일 종가 조회
            final_price = fetch_price_on_date(ticker, MATURITY_DATES[ticker])

            if final_price >= strike * m_barrier:
                payout = strike * (1 + m_coupon)
                body_lines.append(
                    f"  → 만기평가일: {maturity_date}, Barrier≥{m_barrier*100:.1f}% (충족), 상환가={payout:.2f}"
                )
            else:
                body_lines.append(
                    f"  → 만기평가일: {maturity_date}, Barrier<{m_barrier*100:.1f}% (미충족), "
                    f"상환가=기초자산 종가({final_price:.2f})"
                )

        # 차트 첨부
        chart_buf = generate_price_chart(ticker)
        attachments.append((f"{ticker}_chart_{today_str}.png", chart_buf))
        body_lines.append("")  # 한 줄 띄우기

    # 이메일 전송
    send_email(
        subject=f"[{today_str}] ELS Daily Report",
        body="\n".join(body_lines),
        attachments=attachments,
        config=EMAIL_CONFIG
    )

    print(f"[{datetime.now()}] Email sent.")

if __name__ == '__main__':
    job()
    # schedule.every().day.at("09:00").do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(30)
