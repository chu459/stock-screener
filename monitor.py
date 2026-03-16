#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能选股工具健康监控脚本
用于自动化运维监控，确保服务正常运行
"""

import requests
import time
import json
import sys
import os
from datetime import datetime

def check_health(base_url="http://localhost:5000"):
    """检查服务健康状态"""
    try:
        # 健康检查端点
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return True, data
        else:
            return False, {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return False, {"error": str(e)}

def check_stocks_endpoint(base_url="http://localhost:5000"):
    """检查股票数据端点"""
    try:
        response = requests.get(f"{base_url}/api/stocks", timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('count', 0) > 0:
                return True, data
            else:
                return False, data
        else:
            return False, {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return False, {"error": str(e)}

def send_alert(message, level="WARNING"):
    """发送告警（控制台输出，可扩展为邮件/钉钉/微信）"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_msg = f"[{timestamp}] [{level}] {message}"
    print(alert_msg)

    # TODO: 集成告警通知
    # - 邮件通知
    # - 钉钉机器人
    # - 微信通知
    # - 短信通知

    # 简单实现：记录到日志文件
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f"monitor_{datetime.now().strftime('%Y%m%d')}.log")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(alert_msg + "\n")

def run_monitoring_loop(interval_minutes=5, base_url="http://localhost:5000"):
    """运行监控循环"""
    print(f"启动智能选股工具监控服务，检查间隔：{interval_minutes}分钟")
    print(f"监控地址：{base_url}")
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    consecutive_failures = 0
    max_consecutive_failures = 3

    while True:
        try:
            # 健康检查
            health_ok, health_data = check_health(base_url)

            # 数据端点检查
            stocks_ok, stocks_data = check_stocks_endpoint(base_url)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if health_ok and stocks_ok:
                consecutive_failures = 0
                stock_count = stocks_data.get('count', 0)
                cache_age = health_data.get('cache_age', 'unknown')

                status_msg = f"✅ 服务正常 | 股票数量：{stock_count} | 缓存状态：{cache_age}"
                print(f"[{timestamp}] {status_msg}")

                # 记录详细状态（每小时一次）
                current_minute = datetime.now().minute
                if current_minute == 0:  # 整点时记录详细状态
                    send_alert(f"整点状态检查：{status_msg}", "INFO")

            else:
                consecutive_failures += 1
                error_details = []
                if not health_ok:
                    error_details.append(f"健康检查失败：{health_data.get('error', '未知错误')}")
                if not stocks_ok:
                    error_details.append(f"数据端点失败：{stocks_data.get('error', '未知错误')}")

                error_msg = " | ".join(error_details)
                alert_msg = f"❌ 服务异常 ({consecutive_failures}/{max_consecutive_failures}): {error_msg}"

                print(f"[{timestamp}] {alert_msg}")
                send_alert(alert_msg, "ERROR")

                # 连续失败超过阈值，发送紧急告警
                if consecutive_failures >= max_consecutive_failures:
                    emergency_msg = f"🚨 服务连续失败 {consecutive_failures} 次，需要立即检查！"
                    send_alert(emergency_msg, "CRITICAL")

            # 等待下一个检查周期
            time.sleep(interval_minutes * 60)

        except KeyboardInterrupt:
            print("\n监控服务已停止")
            break
        except Exception as e:
            error_msg = f"监控循环异常：{str(e)}"
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}")
            send_alert(error_msg, "ERROR")
            time.sleep(interval_minutes * 60)

def generate_report(base_url="http://localhost:5000"):
    """生成监控报告"""
    print("生成监控报告...")

    report = {
        "timestamp": datetime.now().isoformat(),
        "health_check": {},
        "performance_check": {}
    }

    # 健康检查
    health_ok, health_data = check_health(base_url)
    report["health_check"] = {
        "status": "healthy" if health_ok else "unhealthy",
        "data": health_data
    }

    # 性能检查
    import time as ttime
    start_time = ttime.time()
    stocks_ok, stocks_data = check_stocks_endpoint(base_url)
    response_time = ttime.time() - start_time

    report["performance_check"] = {
        "status": "ok" if stocks_ok else "failed",
        "response_time_seconds": round(response_time, 3),
        "stock_count": stocks_data.get('count', 0) if stocks_ok else 0,
        "data": stocks_data if stocks_ok else {"error": stocks_data.get('error')}
    }

    # 保存报告
    report_dir = "reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    report_file = os.path.join(report_dir, f"monitor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"报告已保存至：{report_file}")
    return report_file

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='智能选股工具健康监控')
    parser.add_argument('--url', default='http://localhost:5000', help='服务基础URL')
    parser.add_argument('--interval', type=int, default=5, help='检查间隔（分钟）')
    parser.add_argument('--report', action='store_true', help='生成报告后退出')
    parser.add_argument('--once', action='store_true', help='单次检查后退出')

    args = parser.parse_args()

    if args.report:
        report_file = generate_report(args.url)
        print(f"监控报告生成完成：{report_file}")
    elif args.once:
        print("执行单次检查...")
        health_ok, health_data = check_health(args.url)
        stocks_ok, stocks_data = check_stocks_endpoint(args.url)

        if health_ok and stocks_ok:
            print(f"✅ 服务正常 | 股票数量：{stocks_data.get('count', 0)}")
            sys.exit(0)
        else:
            print(f"❌ 服务异常")
            if not health_ok:
                print(f"   健康检查失败：{health_data.get('error')}")
            if not stocks_ok:
                print(f"   数据端点失败：{stocks_data.get('error')}")
            sys.exit(1)
    else:
        run_monitoring_loop(args.interval, args.url)