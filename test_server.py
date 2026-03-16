#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试智能选股工具服务器
"""
import subprocess
import time
import requests
import json
import sys
import os

def run_tests():
    print("🚀 启动智能选股工具服务器测试...")

    # 启动服务器子进程
    server_proc = subprocess.Popen(
        [sys.executable, 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

    # 等待服务器启动
    print("等待服务器启动（5秒）...")
    time.sleep(5)

    base_url = 'http://localhost:5000'
    tests_passed = 0
    tests_failed = 0

    try:
        # 测试1: 健康检查
        print("\n1. 测试健康检查端点...")
        try:
            resp = requests.get(f'{base_url}/api/health', timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    print("   ✓ 健康检查通过")
                    tests_passed += 1
                else:
                    print(f"   ✗ 健康检查失败: {data.get('error')}")
                    tests_failed += 1
            else:
                print(f"   ✗ HTTP错误: {resp.status_code}")
                tests_failed += 1
        except Exception as e:
            print(f"   ✗ 请求失败: {e}")
            tests_failed += 1

        # 测试2: 获取股票数据
        print("\n2. 测试股票数据端点...")
        try:
            resp = requests.get(f'{base_url}/api/stocks', timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    count = data.get('count', 0)
                    print(f"   ✓ 获取股票数据成功，共 {count} 只股票")
                    tests_passed += 1
                else:
                    print(f"   ✗ 获取股票数据失败: {data.get('error')}")
                    tests_failed += 1
            else:
                print(f"   ✗ HTTP错误: {resp.status_code}")
                tests_failed += 1
        except Exception as e:
            print(f"   ✗ 请求失败: {e}")
            tests_failed += 1

        # 测试3: 筛选股票
        print("\n3. 测试股票筛选端点...")
        try:
            conditions = {
                'min_price': 10,
                'max_price': 100,
                'min_volume': 10000,
                'max_pe': 30,
                'limit': 5
            }
            resp = requests.post(
                f'{base_url}/api/screener',
                json={'conditions': conditions},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    filtered_count = data.get('count', 0)
                    print(f"   ✓ 筛选成功，找到 {filtered_count} 只符合条件的股票")
                    tests_passed += 1
                else:
                    print(f"   ✗ 筛选失败: {data.get('error')}")
                    tests_failed += 1
            else:
                print(f"   ✗ HTTP错误: {resp.status_code}")
                tests_failed += 1
        except Exception as e:
            print(f"   ✗ 请求失败: {e}")
            tests_failed += 1

        # 测试4: 生成报告
        print("\n4. 测试报告生成端点...")
        try:
            # 先获取一些数据
            resp = requests.get(f'{base_url}/api/stocks', timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success') and data.get('data'):
                    sample_data = data['data'][:3]

                    resp2 = requests.post(
                        f'{base_url}/api/report',
                        json={'data': sample_data, 'type': 'json'},
                        timeout=10
                    )
                    if resp2.status_code == 200:
                        report_data = resp2.json()
                        if report_data.get('success'):
                            print(f"   ✓ JSON报告生成成功，包含 {report_data.get('count', 0)} 只股票")
                            tests_passed += 1
                        else:
                            print(f"   ✗ 报告生成失败: {report_data.get('error')}")
                            tests_failed += 1
                    else:
                        print(f"   ✗ HTTP错误: {resp2.status_code}")
                        tests_failed += 1
                else:
                    print("   ✗ 没有可用的股票数据")
                    tests_failed += 1
        except Exception as e:
            print(f"   ✗ 请求失败: {e}")
            tests_failed += 1

        # 测试5: 首页访问
        print("\n5. 测试首页访问...")
        try:
            resp = requests.get(base_url, timeout=5)
            if resp.status_code == 200:
                print("   ✓ 首页访问成功")
                tests_passed += 1
            else:
                print(f"   ✗ HTTP错误: {resp.status_code}")
                tests_failed += 1
        except Exception as e:
            print(f"   ✗ 请求失败: {e}")
            tests_failed += 1

    finally:
        # 停止服务器
        print("\n🛑 停止服务器...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()

        # 输出服务器日志
        stdout, stderr = server_proc.communicate()
        if stdout:
            print("\n服务器标准输出:")
            print(stdout.decode('utf-8', errors='ignore'))
        if stderr:
            print("\n服务器标准错误:")
            print(stderr.decode('utf-8', errors='ignore'))

    # 测试总结
    print(f"\n{'='*50}")
    print("测试总结:")
    print(f"  通过: {tests_passed}")
    print(f"  失败: {tests_failed}")
    print(f"  总计: {tests_passed + tests_failed}")

    if tests_failed == 0:
        print("\n🎉 所有测试通过！智能选股工具MVP已就绪。")
        return True
    else:
        print("\n⚠️  部分测试失败，需要检查。")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)