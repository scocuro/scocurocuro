# config.py
# ELS Daily Report configuration

from datetime import date

UNDERLYING_TICKERS = ['^N225', '^GSPC', '^KS200','PLTR','MU']

STRIKE_PRICES = {
    '^N225': 51939.89,
    '^GSPC': 6966.28,
    '^KS200': 1477.22,
    'PLTR': 177.49,
    'MU' : 345.09,    
}

# 3) 차수별 Barrier 비율
EARLY_REDEMPTION_BARRIERS = {
    # 제455회 ELS (지수)
    '^N225': {
         1: 0.85,
         2: 0.85,
         3: 0.85,
         4: 0.80,
         5: 0.80,
         6: 0.80,
         7: 0.75,
         8: 0.75,
         9: 0.7,
         10: 0.7,
         11: 0.7,
         12: 0.7,# 만기평가일 Barrier
    },
    '^GSPC': {
         1: 0.85,
         2: 0.85,
         3: 0.85,
         4: 0.80,
         5: 0.80,
         6: 0.80,
         7: 0.75,
         8: 0.75,
         9: 0.7,
         10: 0.7,
         11: 0.7,
         12: 0.7,# 만기평가일 Barrier
    },
    '^KS200': {
         1: 0.85,
         2: 0.85,
         3: 0.85,
         4: 0.80,
         5: 0.80,
         6: 0.80,
         7: 0.75,
         8: 0.75,
         9: 0.7,
         10: 0.7,
         11: 0.7,
         12: 0.7,# 만기평가일 Barrier
    },
    'PLTR': {
         1: 0.80,
         2: 0.75,
         3: 0.75,
         4: 0.75,
         5: 0.60,
         6: 0.55,
    },
    'MU': {
         1: 0.80,
         2: 0.75,
         3: 0.75,
         4: 0.75,
         5: 0.60,
         6: 0.55,
    },
}

# 4) 차수별 Coupon 연율
EARLY_REDEMPTION_COUPONS = {
    '^N225':    {i: 0.229 for i in range(1,12)},
    '^GSPC':    {i: 0.0880 for i in range(1,12)},
    '^KS200':{i: 0.0880 for i in range(1,612},
    'PLTR':{i: 0.22 for i in range(1,6)},
    'MU':{i: 0.22 for i in range(1,6)},
}

# 5) 티커별 평가일
EVALUATION_DATES = {
    # 제15회 ELS (지수): 5차만 운영, 만기평가일 없음
    '^N225':  {1:date(2026,9,18),2:date(2026, 12,22),3:date(2027,3,19),4:date(2027,6,22),5:date(2027,9,22),6:date(2027,12,22),7:date(2028,3,22),8:date(2028,6,22),9:date(2028,9,21),10:date(2028,12,22),11:date(2028,,22)},
    '^GSPC':  {1:date(2026,7,9),2:date(2027, 1,8),3:date(2027,7,9),4:date(2028,1,7),5:date(2028,7,7)},
    '^KS200':{1:date(2026,7,9),2:date(2027, 1,8),3:date(2027,7,9),4:date(2028,1,7),5:date(2028,7,7)},
    'PLTR':{1:date(2026,7,9),2:date(2027, 1,8),3:date(2027,7,9),4:date(2028,1,7),5:date(2028,7,7)},
    'MU':{1:date(2026,7,9),2:date(2027, 1,8),3:date(2027,7,9),4:date(2028,1,7),5:date(2028,7,7)},
}

# 6) Knock-in Barrier 비율
KNOCK_IN_BARRIERS = {
    '^N225':  0.35,
    '^GSPC':  0.35,
    '^KS200': 0.35,
    'PLTR': 44.3725/177.49,
    'MU': 86.2725/345.09,
}

# ◼︎ 별도 만기일 매핑 (실제 만기일로 바꿔 주세요)
MATURITY_DATES = {
  '^N225':   date(2029,6,27),
  '^GSPC':   date(2029,6,27),
  '^KS200':date(2029,6,27),
  'PLTR':date(2029,1,9),
  'MU':date(2029,1,9),
}
    
# 8) 만기 평가일의 Barrier 비율 (Redemption Barrier at Maturity)
MATURITY_BARRIERS = {
    '^N225':     0.70,
    '^GSPC':     0.70,
    '^KS200': 0.70,
    'PLTR': 0.55,
    'MU': 0.55,
}

# 9) 만기 쿠폰 연율 (Final Coupon at Maturity)
MATURITY_COUPONS = {
    '^N225':    0.229,
    '^GSPC':    0.229,
    '^KS200':0.229,
    'PLTR': 0.22,
    'MU': 0.22,
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
    '^KS200': 'KOSPI200(^KS200)',
    'PLTR': '팔란티어(PLTR)',
    'MU': '마이크론테크놀로지(MU)'
}
