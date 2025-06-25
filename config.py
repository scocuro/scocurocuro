# config.py
# ELS Daily Report configuration

UNDERLYING_TICKERS = ['PLTR', 'TSLA', '^N225', '^GSPC', '^STOXX50E']

STRIKE_PRICES = {
    'PLTR': 137.30,
    'TSLA': 322.16,
    '^N225': 38403.23,
    '^GSPC': 5967.84,
    '^STOXX50E': 5233.58
}

EARLY_REDEMPTION_BARRIERS = {
    'PLTR': {1: 0.75, 2: 0.75, 3: 0.75, 4: 0.70, 5: 0.70},
    'TSLA': {1: 0.75, 2: 0.75, 3: 0.75, 4: 0.70, 5: 0.70},
    '^N225': {1: 0.90, 2: 0.85, 3: 0.85, 4: 0.80, 5: 0.80},
    '^GSPC': {1: 0.90, 2: 0.85, 3: 0.85, 4: 0.80, 5: 0.80},
    '^STOXX50E': {1: 0.90, 2: 0.85, 3: 0.85, 4: 0.80, 5: 0.80}
}

EARLY_REDEMPTION_COUPONS = {
    'PLTR': {i: 0.2301 for i in range(1, 6)},
    'TSLA': {i: 0.2301 for i in range(1, 6)},
    '^N225': {i: 0.0930 for i in range(1, 6)},
    '^GSPC': {i: 0.0930 for i in range(1, 6)},
    '^STOXX50E': {i: 0.0930 for i in range(1, 6)}
}

EMAIL_CONFIG = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    'USERNAME': 'hyunseo.kang238@gmail.com',
    'PASSWORD': 'ufrqdcgbcryicxvo',
    'FROM_ADDR': 'hyunseo.kang238@gmail.com',
    'TO_ADDRS': ['fan155@naver.com']
}
