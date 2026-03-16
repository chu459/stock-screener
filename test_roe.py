#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from screener_data import get_roe_from_akshare

# 测试几个股票
test_cases = [
    ('000001', 'sz'),  # 平安银行
    ('600519', 'sh'),  # 贵州茅台
]

for code, market in test_cases:
    roe = get_roe_from_akshare(code, market)
    if roe is not None:
        print(f"{market}{code} ROE: {roe:.2f}%")
    else:
        print(f"{market}{code} ROE: 获取失败")