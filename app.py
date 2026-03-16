#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能选股工具后端API服务器
"""
import json
import os
import sys
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from datetime import datetime
import tempfile
import threading

# 添加当前目录到模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入数据模块
from screener_data import load_stock_list, fetch_stock_data, filter_stocks

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # 允许跨域请求

# 全局缓存股票数据（简单实现）
stock_data_cache = {'timestamp': None, 'data': []}
CACHE_DURATION = 300  # 缓存5分钟

def get_cached_stock_data(force_refresh=False):
    """获取缓存的股票数据，必要时刷新"""
    global stock_data_cache

    now = datetime.now().timestamp()

    if (force_refresh or
        not stock_data_cache['timestamp'] or
        now - stock_data_cache['timestamp'] > CACHE_DURATION):

        print("刷新股票数据缓存...")
        try:
            # 加载股票列表
            stocks_file = os.path.join(os.path.dirname(__file__), 'stocks.txt')
            stock_codes = load_stock_list(stocks_file)

            # 获取数据
            data = fetch_stock_data(stock_codes)
            stock_data_cache = {
                'timestamp': now,
                'data': data
            }
            print(f"数据缓存已更新，共 {len(data)} 只股票")
        except Exception as e:
            print(f"刷新缓存失败: {e}")
            if not stock_data_cache['data']:
                raise

    return stock_data_cache['data']

@app.route('/')
def index():
    """首页，返回前端页面"""
    return render_template('index.html')

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """获取股票数据"""
    try:
        force = request.args.get('force', 'false').lower() == 'true'
        data = get_cached_stock_data(force_refresh=force)
        return jsonify({'success': True, 'count': len(data), 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/screener', methods=['POST'])
def screener():
    """筛选股票"""
    try:
        # 获取筛选条件
        conditions = request.json.get('conditions', {})

        # 获取股票数据
        data = get_cached_stock_data()

        # 筛选股票
        filtered = filter_stocks(data, conditions)

        # 排序（默认按涨跌幅降序）
        sort_by = conditions.get('sort_by', 'change_percent')
        reverse = conditions.get('sort_desc', True)

        def sort_key(stock):
            try:
                return float(stock.get(sort_by, 0))
            except:
                return 0

        filtered.sort(key=sort_key, reverse=reverse)

        # 限制返回数量
        limit = conditions.get('limit', 50)
        if limit > 0:
            filtered = filtered[:limit]

        return jsonify({
            'success': True,
            'count': len(filtered),
            'total': len(data),
            'data': filtered
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/report', methods=['POST'])
def generate_report():
    """生成筛选报告（PDF或Excel）"""
    try:
        data = request.json.get('data', [])
        report_type = request.json.get('type', 'json')

        if not data:
            return jsonify({'success': False, 'error': '没有数据可生成报告'}), 400

        if report_type == 'json':
            # 返回JSON数据
            return jsonify({
                'success': True,
                'type': 'json',
                'data': data,
                'count': len(data)
            })
        elif report_type == 'csv':
            # 生成CSV文件
            import csv
            import io

            output = io.StringIO()
            writer = csv.writer(output)

            # 表头
            headers = ['代码', '名称', '市场', '价格', '涨跌幅', '成交量(手)', 'PE', 'ROE(%)', '市值', '时间']
            writer.writerow(headers)

            # 数据行
            for stock in data:
                row = [
                    stock.get('code', ''),
                    stock.get('name', ''),
                    stock.get('market', ''),
                    stock.get('price', 0),
                    stock.get('change_percent', '0%'),
                    stock.get('volume', 0),
                    stock.get('pe', 0),
                    stock.get('roe', 0),
                    stock.get('market_cap', 0),
                    stock.get('timestamp', '')
                ]
                writer.writerow(row)

            csv_content = output.getvalue()
            output.close()

            # 保存临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
                f.write(csv_content)
                temp_path = f.name

            return send_file(
                temp_path,
                as_attachment=True,
                download_name=f'stock_screener_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mimetype='text/csv'
            )
        else:
            return jsonify({'success': False, 'error': f'不支持的报告类型: {report_type}'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'cache_age': 'fresh' if stock_data_cache['timestamp'] else 'empty'
    })

def run_background_refresh():
    """后台定时刷新数据"""
    def refresh():
        import time
        while True:
            try:
                get_cached_stock_data(force_refresh=True)
            except Exception as e:
                print(f"后台刷新失败: {e}")
            time.sleep(600)  # 每10分钟刷新一次

    thread = threading.Thread(target=refresh, daemon=True)
    thread.start()

if __name__ == '__main__':
    # 启动后台刷新线程
    run_background_refresh()

    # 启动Flask应用
    port = int(os.environ.get('PORT', 5000))
    print("智能选股工具后端API服务器启动...")
    print(f"访问 http://localhost:{port} 使用选股工具")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)