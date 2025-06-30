import schedule
import time
from datetime import date
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
import os
import sys

def job():
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')

    # 환경 변수 출력 (디버깅용)
    print("SMTP_SERVER:", os.getenv('SMTP_SERVER'))
    print("SMTP_PORT:", os.getenv('SMTP_PORT'))
    print("EMAIL_USER:", os.getenv('EMAIL_USER'))
    print("EMAIL_PASS:", os.getenv('EMAIL_PASS'))
    print("EMAIL_FROM:", os.getenv('EMAIL_FROM'))
    print("EMAIL_TO:", os.getenv('EMAIL_TO'))

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
            barrier = EARLY_REDEMPTION_BARRIERS[ticker]

            # 테이블에 데이터를 추가
            rows.append([ticker, close_price, strike, decline_txt, ki_price, upcoming, eval_date, barrier, EARLY_REDEMPTION_COUPONS[ticker]])

    # 이메일 전송 전 로그 추가
    print("Sending email with the following data:")
    for row in rows:
        print(row)

    # 이메일 발송
    send_email(
        subject=f"ELS Report ({today_str})",
        body="아래는 ELS 리포트 내용입니다:\n" + "\n".join([", ".join(map(str, row)) for row in rows]),
        attachments=[("els_report.csv", "path_to_your_report.csv")],
        config=EMAIL_CONFIG
    )

# 자동 실행: 스케줄러 설정 (매일 특정 시간에 실행되도록)
def schedule_job():
    schedule.every().day.at("07:10").do(job)  # 7:10 AM (한국 시간)에 실행

    # 반복 실행 없이 일정 시간이 지난 후 종료
    while True:
        print("Waiting for scheduled jobs...")
        schedule.run_pending()
        time.sleep(60)  # 1분마다 실행
        if schedule.get_jobs() == []:  # 모든 작업이 끝났다면 종료
            print("All jobs completed, exiting loop.")
            break

# 매뉴얼 실행: 한 번만 실행하고 종료
def manual_run():
    job()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "manual":
        # 매뉴얼 실행 시 한 번만 실행
        print("Manual execution triggered")
        manual_run()
    else:
        # 자동 실행 (GitHub Actions 등에서 사용)
        print("Scheduled execution triggered")
        schedule_job()
