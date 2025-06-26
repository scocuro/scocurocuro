# config.py
# ELS Daily Report configuration

from datetime import date

UNDERLYING_TICKERS = ['PLTR', 'TSLA', '^N225', '^GSPC', '^STOXX50E']

STRIKE_PRICES = {
    'PLTR': 137.30,
    'TSLA': 322.16,
    '^N225': 38403.23,
    '^GSPC': 5967.84,
    '^STOXX50E': 5233.58
}

# 3) 차수별 Barrier 비율
EARLY_REDEMPTION_BARRIERS = {
    # 제21회 ELS (PLTR·TSLA) — 
    # 1~2차:75%, 3차:(표준75%, 리자드50%), 4~6차:70%, 7~8차:65%
    'PLTR': {
         1:   0.75,
         2:   0.75,
         3: (0.75, 0.50),
         4:   0.70,
         5:   0.70,
         6:   0.70,
         7:   0.65,
         8:   0.65,  # 8차가 만기 평가일
    },
    'TSLA': {
         1:   0.75,
         2:   0.75,
         3: (0.75, 0.50),
         4:   0.70,
         5:   0.70,
         6:   0.70,
         7:   0.65,
         8:   0.65,
    },
    # 제15회 ELS (지수) —
    # 1차:90%, 2~3차:85%, 4차:80%, 5차 만기:70%
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
}
# 4) 차수별 Coupon 연율 (3차만 리자드 쿠폰 tuple 유지)
EARLY_REDEMPTION_COUPONS = {
    'PLTR': {
        1:   0.2301,
        2:   0.2301,
        3: (0.2301, 0.4602),
        4:   0.2301,
        5:   0.2301,
        6:   0.2301,
        7:   0.2301,
        8:   0.2301,
    },
    'TSLA': {
        1:   0.2301,
        2:   0.2301,
        3: (0.2301, 0.4602),
        4:   0.2301,
        5:   0.2301,
        6:   0.2301,
        7:   0.2301,
        8:   0.2301,
    },
    '^N225':    {i: 0.0930 for i in range(1,6)},
    '^GSPC':    {i: 0.0930 for i in range(1,6)},
    '^STOXX50E':{i: 0.0930 for i in range(1,6)},
}

# 5) 티커별 평가일
EVALUATION_DATES = {
    # 제21회 ELS (PLTR·TSLA): 8차
    'PLTR': {
        1: date(2025, 10,20),
        2: date(2026,  2,20),
        3: date(2026,  6,22),
        4: date(2026, 10,20),
        5: date(2027,  2,19),
        6: date(2027, 6,21),
        7: date(2027,  10,20),
        8: date(2028,  2,18),  # 만기평가 (제외됨)
    },
    'TSLA': {
        1: date(2025, 10,20),
        2: date(2026,  2,20),
        3: date(2026,  6,22),
        4: date(2026, 10,20),
        5: date(2027,  2,19),
        6: date(2027, 6,21),
        7: date(2027,  10,20),
        8: date(2028,  2,18),  # 만기평가 (제외됨)
    },
    # 제15회 ELS (지수): 5차만 운영, 만기평가일 없음
    '^N225':  {1:date(2025,12,17),2:date(2026, 6,17),3:date(2026, 12,16),4:date(2027, 6,16),5:date(2027,12,15)},
    '^GSPC':  {1:date(2025,12,17),2:date(2026, 6,17),3:date(2026, 12,16),4:date(2027, 6,16),5:date(2027,12,15)},
    '^STOXX50E':{1:date(2025,12,17),2:date(2026, 6,17),3:date(2026, 12,16),4:date(2027, 6,16),5:date(2027,12,15)},
}

# 6) Knock-in Barrier 비율
KNOCK_IN_BARRIERS = {
    'PLTR':   0.30,
    'TSLA':   0.30,
    '^N225':  0.45,
    '^GSPC':  0.45,
    '^STOXX50E':0.45,
}

# ◼︎ 별도 만기일 매핑 (실제 만기일로 바꿔 주세요)
MATURITY_DATES = {
  'PLTR':    date(2028,2,18),
  'TSLA':    date(2028,2,18),
  '^N225':  date(2028,6,14),
  '^GSPC':  date(2028,6,14),
  '^STOXX50E':date(2028,6,14),
}
    
# 8) 만기 평가일의 Barrier 비율 (Redemption Barrier at Maturity)
MATURITY_BARRIERS = {
    'PLTR':      0.60,
    'TSLA':      0.60,
    '^N225':     0.70,
    '^GSPC':     0.70,
    '^STOXX50E': 0.70,
}

# 9) 만기 쿠폰 연율 (Final Coupon at Maturity)
#    예: 21회는 9번째 쿠폰이 연 23.01%, 15회 지수는 6번째 쿠폰 연 9.30%
MATURITY_COUPONS = {
    'PLTR':   0.2301,
    'TSLA':   0.2301,
    '^N225':  0.0930,
    '^GSPC':  0.0930,
    '^STOXX50E':0.0930,
}
    
EMAIL_CONFIG = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    'USERNAME': 'hyunseo.kang238@gmail.com',
    'PASSWORD': 'ufrqdcgbcryicxvo',
    'FROM_ADDR': 'hyunseo.kang238@gmail.com',
    'TO_ADDRS': ['fan155@naver.com']
}
