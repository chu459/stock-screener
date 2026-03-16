import akshare as ak
import pandas as pd

# 测试其他akshare函数
try:
    # 试试财务摘要
    df = ak.stock_financial_abstract(symbol="000001")
    print("stock_financial_abstract shape:", df.shape)
    print(df.head())
except Exception as e:
    print("stock_financial_abstract error:", e)

# 试试财务指标
try:
    df = ak.stock_financial_analysis_indicator(symbol="000001")
    print("stock_financial_analysis_indicator shape:", df.shape)
    print(df.head())
except Exception as e:
    print("stock_financial_analysis_indicator error:", e)

# 试试利润表
try:
    df = ak.stock_financial_report(symbol="000001", indicator="利润表")
    print("stock_financial_report shape:", df.shape)
    print(df.head())
except Exception as e:
    print("stock_financial_report error:", e)