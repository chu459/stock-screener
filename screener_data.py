#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能选股工具数据获取模块
集成东财Skill获取股票数据

数据说明：
1. 实时行情数据：来自东方财富实时接口（真实数据）
2. 财务数据（PE、ROE、市值）：当前为模拟数据，实际应用需接入：
   - akshare (免费) 或 tushare (需要token) 获取真实财务数据
   - 东方财富财务数据接口
   - 聚宽、米筐等量化平台API
"""
import sys
import os
import json
import time
import random
from typing import List, Dict, Any

# 添加父目录到路径，以便导入eastmoney模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eastmoney.data_fetcher import get_stock_quote

def load_stock_list(file_path: str) -> List[str]:
    """加载股票列表"""
    stocks = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                stocks.append(line)
    return stocks

def fetch_stock_data(stock_codes: List[str], max_concurrent: int = 5) -> List[Dict[str, Any]]:
    """
    批量获取股票数据
    添加简单延迟以避免请求过快
    """
    results = []

    for i, code in enumerate(stock_codes):
        try:
            # 确定市场
            if code.startswith('6'):
                market = 'sh'
            else:
                market = 'sz'

            # 获取数据
            quote = get_stock_quote(code, market)

            if 'error' not in quote:
                # 使用真实财务数据（如果接口提供）
                pe = quote.get('pe', random.uniform(5, 50))
                pb = quote.get('pb', 0.0)
                market_cap = quote.get('market_cap', quote['current'] * random.uniform(1e8, 1e10))
                # ROE暂时使用模拟数据，后续可接入akshare
                roe = random.uniform(5, 25)

                stock_info = {
                    'code': code,
                    'name': quote['name'],
                    'market': market,
                    'price': quote['current'],
                    'change': quote['change'],
                    'change_percent': quote['change_percent'],
                    'volume': quote['volume'],
                    'amount': quote['amount'],
                    'high': quote['high'],
                    'low': quote['low'],
                    'open': quote['open'],
                    'pe': round(pe, 2),
                    'pb': round(pb, 2),
                    'roe': round(roe, 2),
                    'market_cap': round(market_cap, 2),
                    'timestamp': quote['timestamp']
                }
                results.append(stock_info)
                print(f"✓ 获取 {code} 数据成功")
            else:
                print(f"✗ 获取 {code} 数据失败: {quote['error']}")

        except Exception as e:
            print(f"✗ 处理 {code} 时出错: {e}")

        # 添加延迟，避免请求过快
        if i < len(stock_codes) - 1:
            time.sleep(0.5)

    return results

def filter_stocks(stocks: List[Dict[str, Any]], conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    根据条件筛选股票

    支持的条件：
    - min_price: 最低价格
    - max_price: 最高价格
    - min_change_percent: 最小涨跌幅（%）
    - max_change_percent: 最大涨跌幅（%）
    - min_volume: 最小成交量（手）
    - max_pe: 最大市盈率
    - max_pb: 最大市净率
    - min_pb: 最小市净率
    - min_roe: 最小净资产收益率（%）
    - min_market_cap: 最小市值
    - max_market_cap: 最大市值
    """
    filtered = []

    for stock in stocks:
        match = True

        # 价格筛选
        if 'min_price' in conditions and stock['price'] < conditions['min_price']:
            match = False
        if 'max_price' in conditions and stock['price'] > conditions['max_price']:
            match = False

        # 涨跌幅筛选（需要将change_percent转换为浮点数）
        try:
            change_pct = float(stock['change_percent'].strip('%'))
        except:
            change_pct = 0.0

        if 'min_change_percent' in conditions and change_pct < conditions['min_change_percent']:
            match = False
        if 'max_change_percent' in conditions and change_pct > conditions['max_change_percent']:
            match = False

        # 成交量筛选
        if 'min_volume' in conditions and stock['volume'] < conditions['min_volume']:
            match = False

        # PE筛选
        if 'max_pe' in conditions and stock['pe'] > conditions['max_pe']:
            match = False

        # PB筛选
        if 'max_pb' in conditions and stock['pb'] > conditions['max_pb']:
            match = False
        if 'min_pb' in conditions and stock['pb'] < conditions['min_pb']:
            match = False

        # ROE筛选
        if 'min_roe' in conditions and stock['roe'] < conditions['min_roe']:
            match = False

        # 市值筛选
        if 'min_market_cap' in conditions and stock['market_cap'] < conditions['min_market_cap']:
            match = False
        if 'max_market_cap' in conditions and stock['market_cap'] > conditions['max_market_cap']:
            match = False

        if match:
            filtered.append(stock)

    return filtered

def save_results(stocks: List[Dict[str, Any]], file_path: str):
    """保存筛选结果"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)
    print(f"结果已保存到 {file_path}")

def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='智能选股工具数据获取')
    parser.add_argument('--stocks', default='stocks.txt', help='股票列表文件路径')
    parser.add_argument('--output', default='screener_results.json', help='输出文件路径')
    parser.add_argument('--min-price', type=float, help='最低价格')
    parser.add_argument('--max-price', type=float, help='最高价格')
    parser.add_argument('--min-change', type=float, help='最小涨跌幅（%）')
    parser.add_argument('--max-change', type=float, help='最大涨跌幅（%）')
    parser.add_argument('--min-volume', type=int, help='最小成交量（手）')
    parser.add_argument('--max-pe', type=float, help='最大市盈率')
    parser.add_argument('--max-pb', type=float, help='最大市净率')
    parser.add_argument('--min-pb', type=float, help='最小市净率')
    parser.add_argument('--min-roe', type=float, help='最小净资产收益率（%）')
    parser.add_argument('--min-market-cap', type=float, help='最小市值')
    parser.add_argument('--max-market-cap', type=float, help='最大市值')

    args = parser.parse_args()

    # 加载股票列表
    stocks = load_stock_list(args.stocks)
    print(f"加载了 {len(stocks)} 只股票")

    # 获取股票数据
    stock_data = fetch_stock_data(stocks)
    print(f"成功获取 {len(stock_data)} 只股票数据")

    # 构建筛选条件
    conditions = {}
    if args.min_price is not None:
        conditions['min_price'] = args.min_price
    if args.max_price is not None:
        conditions['max_price'] = args.max_price
    if args.min_change is not None:
        conditions['min_change_percent'] = args.min_change
    if args.max_change is not None:
        conditions['max_change_percent'] = args.max_change
    if args.min_volume is not None:
        conditions['min_volume'] = args.min_volume
    if args.max_pe is not None:
        conditions['max_pe'] = args.max_pe
    if args.max_pb is not None:
        conditions['max_pb'] = args.max_pb
    if args.min_pb is not None:
        conditions['min_pb'] = args.min_pb
    if args.min_roe is not None:
        conditions['min_roe'] = args.min_roe
    if args.min_market_cap is not None:
        conditions['min_market_cap'] = args.min_market_cap
    if args.max_market_cap is not None:
        conditions['max_market_cap'] = args.max_market_cap

    # 筛选股票
    filtered_stocks = filter_stocks(stock_data, conditions)
    print(f"筛选出 {len(filtered_stocks)} 只符合条件的股票")

    # 保存结果
    save_results(filtered_stocks, args.output)

    # 打印结果摘要
    if filtered_stocks:
        print("\n筛选结果摘要:")
        for stock in filtered_stocks[:5]:  # 只显示前5只
            print(f"  {stock['code']} {stock['name']}: 价格{stock['price']}元, 涨跌幅{stock['change_percent']}, PE{stock['pe']}, ROE{stock['roe']}%")
        if len(filtered_stocks) > 5:
            print(f"  ... 还有 {len(filtered_stocks)-5} 只股票")

if __name__ == '__main__':
    main()