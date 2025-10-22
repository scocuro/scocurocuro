# config.py
# ELS Daily Report configuration

from datetime import date

UNDERLYING_TICKERS = ['^N225', '^GSPC', '^STOXX50E', '005930.KS', '005380.KS']

STRIKE_PRICES = {
    '^N225': 38403.23,
    '^GSPC': 5967.84,
    '^STOXX50E': 5233.58,
    # 추가: 삼성전자, 현대차 (기준가격)
    '005930.KS': 75400.0,    # 삼성전자 보통주
    '005380.KS': 223500.0,   # 현대차 보통주
}

# 3) 차수별 Barrier 비율
EARLY_REDEMPTION_BARRIERS = {
    # 제15회 ELS (지수)
    # 1차:90%, 2~3차:85%, 4차:80%, 5차 만기:80%
    '^N225': {
         1: 0.90,
         2: 0.85,
         3: 0.85,
         4: 0.80,
         5: 0.80,  # 만기평가일 Barrier
    },
    '^GSPC': {
         1: 0.90,
         2: 0.85,
         3: 0.85,
         4: 0.80,
         5: 0.80,
    },
    '^STOXX50E': {
         1: 0.90,
         2: 0.85,
         3: 0.85,
         4: 0.80,
         5: 0.80,
    },
    # 추가: 삼성전자/현대차 — 6차(평가일 6개), 85/80/80/75/70/60
    '005930.KS': {
         1: 0.85,
         2: 0.80,
         3: 0.80,
         4: 0.75,
         5: 0.70,
         6: 0.60,
    },
    '005380.KS': {
         1: 0.85,
         2: 0.80,
         3: 0.80,
         4: 0.75,
         5: 0.70,
         6: 0.60,
    },
}

# 4) 차수별 Coupon 연율 (3차만 리자드 쿠폰 tuple 유지)
EARLY_REDEMPTION_COUPONS = {
    '^N225':    {i: 0.0930 for i in range(1,6)},
    '^GSPC':    {i: 0.0930 for i in range(1,6)},
    '^STOXX50E':{i: 0.0930 for i in range(1,6)},
    # 추가: 삼성전자/현대차 — 각 차수 10.4%
    '005930.KS': {i: 0.1040 for i in range(1,7)},
    '005380.KS': {i: 0.1040 for i in range(1,7)},
}

# 5) 티커별 평가일
EVALUATION_DATES = {
    # 제15회 ELS (지수): 5차만 운영, 만기평가일 없음
    '^N225':  {1:date(2025,12,17),2:date(2026, 6,17),3:date(2026, 12,16),4:date(2027, 6,16),5:date(2027,12,15)},
    '^GSPC':  {1:date(2025,12,17),2:date(2026, 6,17),3:date(2026, 12,16),4:date(2027, 6,16),5:date(2027,12,15)},
    '^STOXX50E':{1:date(2025,12,17),2:date(2026, 6,17),3:date(2026, 12,16),4:date(2027, 6,16),5:date(2027,12,15)},
    # 추가: 삼성전자/현대차 — 6차 평가일(두 종목 공통)
    '005930.KS': {
        1: date(2026, 3,12),
        2: date(2026, 9,11),
        3: date(2027, 3,12),
        4: date(2027, 9,10),
        5: date(2028, 3,10),
        6: date(2028, 9,15),
    },
    '005380.KS': {
        1: date(2026, 3,12),
        2: date(2026, 9,11),
        3: date(2027, 3,12),
        4: date(2027, 9,10),
        5: date(2028, 3,10),
        6: date(2028, 9,15),
    },
}

# 6) Knock-in Barrier 비율
KNOCK_IN_BARRIERS = {
    '^N225':  0.45,
    '^GSPC':  0.45,
    '^STOXX50E': 0.45,
    # 추가: 삼성전자/현대차 — KI 가격을 기준가로 나눈 비율
    '005930.KS': 33930.0 / 75400.0,   # = 0.45
    '005380.KS': 100575.0 / 223500.0, # = 0.45
}

# ◼︎ 별도 만기일 매핑 (실제 만기일로 바꿔 주세요)
MATURITY_DATES = {
  '^N225':   date(2028,6,14),
  '^GSPC':   date(2028,6,14),
  '^STOXX50E':date(2028,6,14),
  # 추가: 삼성전자/현대차 — 조기상환 마지막일과 동일하게 설정(필요 시 변경)
  '005930.KS': date(2028, 9,15),
  '005380.KS': date(2028, 9,15),
}
    
# 8) 만기 평가일의 Barrier 비율 (Redemption Barrier at Maturity)
MATURITY_BARRIERS = {
    '^N225':     0.70,
    '^GSPC':     0.70,
    '^STOXX50E': 0.70,
    # 추가: 삼성전자/현대차 — 6차 기준 60%와 일치
    '005930.KS': 0.60,
    '005380.KS': 0.60,
}

# 9) 만기 쿠폰 연율 (Final Coupon at Maturity)
#    예: 21회는 9번째 쿠폰이 연 23.01%, 15회 지수는 6번째 쿠폰 연 9.30%
MATURITY_COUPONS = {
    '^N225':    0.0930,
    '^GSPC':    0.0930,
    '^STOXX50E':0.0930,
    # 추가: 삼성전자/현대차 — 10.4%
    '005930.KS': 0.1040,
    '005380.KS': 0.1040,
}
    
EMAIL_CONFIG = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    'USERNAME': 'hyunseo.kang238@gmail.com',
    'PASSWORD': 'ufrqdcgbcryicxvo',
    'FROM_ADDR': 'hyunseo.kang238@gmail.com',
    'TO_ADDRS': ['fan155@naver.com','leejy_93@naver.com']
}

# config.py (맨 아래에 추가)
TICKER_DISPLAY_NAMES = {
    '^N225': '니케이225(^N225)',
    '^GSPC': 'S&P500(^GSPC)',
    '^STOXX50E': '유로스톡스50(^STOXX50E)',
    '005930.KS': '삼성전자(005930.KS)',
    '005380.KS': '현대차(005380.KS)',
}
